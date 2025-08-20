from rest_framework import viewsets, permissions, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import permissions 
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response


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
        # get the followers o
        following_users = request.user.followers.all()
        # fetch the posts from those followers
        posts_from_followers = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = PostSerializer(posts_from_followers, many=True)
        return Response(serializer.data)
