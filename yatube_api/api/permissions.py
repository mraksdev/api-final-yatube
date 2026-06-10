from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthenticatedAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Combined permission: auth check + author-only write.

    Inherits IsAuthenticatedOrReadOnly for has_permission:
    anonymous requests get read-only access.
    On top of that, has_object_permission restricts write/delete
    to the object's author.
    """

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        instance: Model,
    ) -> bool:
        """Allow write/delete only for the object author.

        Safe methods are already permitted by the parent class.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or instance.author == request.user
        )
