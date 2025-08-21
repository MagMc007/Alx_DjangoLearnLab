from rest_framework import viewsets, permissions, filters
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from notifications.models import Notification
from rest_framework import status
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType



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
        # Save the comment with the current user as author
        comment = serializer.save(author=self.request.user)

        # Create a notification for the post's author (if the commenter is not the author)
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                target_content=ContentType.objects.get_for_model(comment),
                target_object_id=comment.id,
            )
    

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


class LikeView(generics.GenericAPIView):
    """ handles liking a post """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)  # get the post to like 
        
        like, created = Like.objects.get_or_create(user=request.user, post=post) # create the like 
        # Prevent multiple likes
        if not created:
            return Response({"detail": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )
        return Response({"detail": "Post liked successfully!"}, status=status.HTTP_201_CREATED)


class UnLikeView(generics.GenericAPIView):
    """ deleting a like """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = get_object_or_404(Like, post=post.id, user=request.user)
        like.delete()
        return Response({"detail": "Unliked successfully"}, status=status.HTTP_200_OK)

