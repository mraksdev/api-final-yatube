from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

UserModel = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model.

    Exposes all post fields. Author is read-only and displayed
    as username via SlugRelatedField.
    """

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model.

    Author is read-only (username). Post is read-only and set
    automatically from the URL parameter.
    """

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model (read-only)."""

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for Follow model.

    User is read-only (username). Following accepts a username
    string as input and validates against self-follow attempts.
    """

    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=UserModel.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate_following(self, following_user: UserModel) -> UserModel:
        """Prevent users from subscribing to themselves.

        Args:
            following_user: User instance being followed.

        Returns:
            The same User instance if validation passes.

        Raises:
            ValidationError: If the user tries to follow themselves.
        """
        request = self.context.get('request')
        if request and following_user == request.user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return following_user

    def validate(self, attrs):
        """Check for duplicate follow before saving.

        Args:
            attrs: Dictionary of validated field values.

        Returns:
            Validated attrs if no duplicate exists.

        Raises:
            ValidationError: If a follow from this user
            to this target already exists.
        """
        request = self.context.get('request')
        following_user = attrs.get('following')
        if (
            request
            and following_user
            and request.user.subscriptions.filter(
                following=following_user
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return attrs
