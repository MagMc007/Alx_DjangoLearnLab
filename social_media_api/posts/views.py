from rest_framework import viewsets, permissions, filters
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from notifications.models import Notification
from rest_framework import status
from django.shortcuts import get_object_or_404


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission for Only the author to edit or delete an object.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """ api view for post """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content'] 
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    """ api view for commenting """
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(APIView):
    """ to handle follower post feed """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # get the followers 
        following_users = request.user.following.all()
        # fetch the posts from those followers
        posts_from_followers = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = PostSerializer(posts_from_followers, many=True)
        return Response(serializer.data)


class LikeView(APIView):
    """ handles liking a post """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)  # get the post to like 
        target_user = request.user   # get the user liking the post
        # Prevent multiple likes
        if Like.objects.filter(post=post, liked_by=target_user).exists():
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(post=post, liked_by=target_user) # create the like 

        if post.author != target_user:  # assuming Post has `author` field
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
        return Response({"detail": "Post liked successfully!"}, status=status.HTTP_201_CREATED)


class UnLikeView(APIView):
    """ deleting a like """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        target_user = request.user
        like = Like.objects.filter(post=post, liked_by=target_user)
        if not like:
            return Response({"detail": "You did not like the post"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"detail": "Unliked successfully"}, status=status.HTTP_200_OK)

