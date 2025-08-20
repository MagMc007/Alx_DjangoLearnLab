from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """ serializes comment data """
    class Meta:
        model = Comment
        fields = ["content"]


class PostSerializer(serializers.ModelSerializer):
    """ serializes post data """
    comments = CommentSerializer(read_only=True, many=True, source="commented_on")

    class Meta:
        model = Post
        fields = ["id", "title", "author", "content",]

