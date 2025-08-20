from rest_framework import serializers
from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    """ serializes comment data """
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content"]


class PostSerializer(serializers.ModelSerializer):
    """ serializes post data """
    comments = CommentSerializer(read_only=True, many=True, source="commented_on")
    likes_count = serializers.IntegerField(source="liked.count", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "author", "content", "comments", "likes_count",]


class LikeSerializer(serializers.ModelSerializer):
    """ serealizes like data"""
    class Meta:
        model = Like
        fields = "__all__"