from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions

class RegisterView(generics.CreateAPIView):
    """ api view for user creations/ registry """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    # override create method and verify token
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        token, created = Token.objects.get_or_create(user=user)
        return Response({"user": response.data, "token":token.key}, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):
    """ login user with valid credentials and check token """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data})


class ProfileView(generics.RetrieveAPIView):
    """ user profile """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        print("User:", self.request.user)  
        print("Auth:", self.request.auth)
        return self.request.user
    

class FollowUserView(generics.GenericAPIView):
    """ implements user following an other user """
    permission_classes = [permissions.IsAuthenticated]  # user must be logged in
    queryset = User.objects.all()

    def post(self, request, user_id):  # user_id = whom other user want to follow
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if target_user == request.user:
            return Response({"error": "You cannot follow yourself"}, status=400)

        if target_user in request.user.following.all():
            return Response({"error": "You already follow this user"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)  
        return Response({"message": f"You are now following {target_user.username}"})

   
class UnfollowUserView(generics.GenericAPIView):
    """ implements user unfollowing another """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if target_user == request.user:
            return Response({"error": "You cannot unfollow yourself"}, status=400)
        
        if target_user not in request.user.following.all():
            return Response({"error": "You do not follow this user"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target_user)
        return Response({"message": f"You unfollowed {target_user.username}"})