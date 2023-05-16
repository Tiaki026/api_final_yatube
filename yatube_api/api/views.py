from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticated)
from posts.models import Post, Group
from .serializers import (
    PostSerializer, GroupSerializer,
    CommentSerializer, FollowSerializer)
from rest_framework.filters import SearchFilter
from .permissions import OnlyAuthorCanModify


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет поста."""

    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [OnlyAuthorCanModify]

    def perform_create(self, serializer) -> None:
        """Переопределение метода perform_create."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет группы."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментария."""

    serializer_class = CommentSerializer
    permission_classes = [OnlyAuthorCanModify]

    def get_post(self) -> Post:
        """Переопределение метода get_post."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self) -> any:
        """Переопределение метода get_queryset."""
        return self.get_post().comments.select_related('author')

    def perform_create(self, serializer) -> None:
        """Переопределение метода perform_create."""
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет подписок."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self) -> any:
        return self.request.user.follower.all()

    def perform_create(self, serializer) -> any:
        return serializer.save(user=self.request.user)
