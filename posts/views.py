from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Comment, Like
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import (
    PostSerializer,
    CommentPostSerializer,
    ImagesPostSerializer
)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        elif self.action in ["list", "retrieve"]:
            return []

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=self.request.user)
        # добавление фотографий в пост
        for image in request.FILES.getlist('images'):
            data = {'image': image, 'post': post.id}
            serializer = ImagesPostSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments

    def perform_create(self, serializer):
        serializer.save(
            post_id=self.kwargs['post_id'],
            author=self.request.user
        )


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if not Like.objects.filter(post=post, author=request.user).exists():
            Like.objects.create(post=post, author=request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        post = Post.objects.get(id=post_id)
        Like.objects.filter(post=post, author=request.user).delete()
        return Response(status=status.HTTP_200_OK)
