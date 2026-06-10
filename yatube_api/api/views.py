from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.serializers import BaseSerializer

from api.permissions import IsAuthenticatedAuthorOrReadOnly
from api.serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer,
)
from posts.models import Follow, Group, Post, Comment


class BaseAuthorViewSet(viewsets.ModelViewSet):
    """Base viewset for models with an author field.

    Provides IsAuthenticatedAuthorOrReadOnly (auth + author-only write)
    and sets the author to the current user on creation.
    """

    permission_classes = (IsAuthenticatedAuthorOrReadOnly,)

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Set the author to the current authenticated user.

        Args:
            serializer: Validated serializer instance.
        """
        serializer.save(author=self.request.user)


class PostViewSet(BaseAuthorViewSet):
    """ViewSet for Post CRUD operations.

    Supports pagination via limit/offset params.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(BaseAuthorViewSet):
    """ViewSet for Comment CRUD, nested under posts.

    Comments are scoped to a specific post via post_id URL kwarg.
    Pagination is disabled — returns a flat list.
    """

    serializer_class = CommentSerializer
    pagination_class = None

    def get_queryset(self) -> QuerySet[Comment]:
        """Filter comments to those belonging to the specified post.

        Returns:
            QuerySet of comments for the post.

        Raises:
            Http404: If the post does not exist.
        """
        return get_object_or_404(
            Post, id=self.kwargs.get('post_id')
        ).comments.all()

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Create a comment linked to the post from the URL.

        Sets both author and post automatically.

        Args:
            serializer: Validated serializer instance.

        Raises:
            Http404: If the post does not exist.
        """
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only ViewSet for Group listing and retrieval.

    Pagination is disabled — returns a flat list.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet for managing user subscriptions.

    Only authenticated users can access. Supports search by
    followed user's username via ?search= param.
    """

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> QuerySet[Follow]:
        """Return only follows belonging to the current user.

        Returns:
            QuerySet of Follow objects where user is the requester.
        """
        return self.request.user.subscriptions.all()

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Create a follow for the current user.

        Args:
            serializer: Validated serializer instance.
        """
        serializer.save(user=self.request.user)
