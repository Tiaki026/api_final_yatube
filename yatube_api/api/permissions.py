from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class OnlyAuthorCanModify(IsAuthenticatedOrReadOnly):
    """Только для чтения, кроме автора."""

    def has_object_permission(self, request, view, obj) -> True or any:
        """Редактировать может только автор."""
        return request.method in SAFE_METHODS or obj.author == request.user
