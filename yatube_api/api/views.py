from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework import pagination
from rest_framework import mixins

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (PostSerializer, CommentSerializer,
                          GroupSerializer, FollowSerializer)
from .permissions import AuthorOrReadOnly

from posts.models import Post, Comment, Group, Follow

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter, filters.OrderingFilter
    ]
    filterset_fields = ('text', 'author')
    search_fields = ('text', 'author__username')
    ordering_fields = ('text', 'author')

    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        if post.pk == comment.post.pk:
            instance.delete()

    def perform_update(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        if post.pk == comment.post.pk:
            serializer.save()

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class FollowViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    search_fields = ('following__username',)

    def get_queryset(self):
        follower = self.request.user
        return Follow.objects.filter(user=follower)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
