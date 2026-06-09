from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission: full access for author, read-only for others.

    Safe methods (GET, HEAD, OPTIONS) are always allowed.
    Write/delete methods are only allowed if the requesting user
    is the author of the object.
    """

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        instance: Model,
    ) -> bool:
        """Check if user can modify the object.

        Args:
            request: The incoming HTTP request.
            view: The view handling the request.
            instance: The model instance being accessed.

        Returns:
            True if the method is safe or the user is the author,
            False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return instance.author == request.user
