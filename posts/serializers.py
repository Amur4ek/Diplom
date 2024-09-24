from rest_framework import serializers

from posts.models import Comment, Post, PostImage


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'text', 'created_at']


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']


class ImagesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['post', 'image']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    images = ImagesPostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'images', 'created_at', 'comments']

    def to_representation(self, post):
        representation = super().to_representation(post)
        representation['likes_count'] = post.likes.count()
        return representation
