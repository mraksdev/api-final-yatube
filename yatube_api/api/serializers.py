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
        """Validate following field: no self-follow, no duplicates.

        Args:
            following_user: User instance being followed.

        Returns:
            The same User instance if validation passes.

        Raises:
            ValidationError: If trying to follow self or a duplicate.
        """
        request = self.context.get('request')
        if request:
            if following_user == request.user:
                raise serializers.ValidationError(
                    'Нельзя подписаться на самого себя'
                )
            if request.user.subscriptions.filter(
                following=following_user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя'
                )
        return following_user
