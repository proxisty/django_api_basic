from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.contrib.auth.models import User
from .models import Post, Comment
from .paginations import PostPagination, CommentPagination
from .permisisions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CommentList(generics.ListCreateAPIView):
    """Выводит список комментариев"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """Выводит комментарий по id"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


###############
class PostList(generics.ListCreateAPIView):
    """Получение всех статьей с пагинацией.
    Создание статьи.
    Поиск по списку статьей"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = PostPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']
    search_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """Получение конкретной статьи по id"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class CommentForPost(generics.ListAPIView):
    """Получение комментариев для статьи по id, с пагинацией."""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs['pk'])
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if post.owner.id == request.user.id:
                comments = Comment.objects.filter(post=post)
                self.get_queryset()
                pg = CommentPagination()
                page_roles = pg.paginate_queryset(queryset=comments, request=request, view=self)
                serializer = serializers.CommentSerializer(page_roles, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
