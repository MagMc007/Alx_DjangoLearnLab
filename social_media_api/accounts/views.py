from .models import User
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


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


class ProfileView(generics.RetrieveUpdateAPIView):
    """ user profile """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user