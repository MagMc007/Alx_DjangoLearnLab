from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model() 


class UserSerializer(serializers.ModelSerializer):
    """ serializes only user info """
    # implement follow logic
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
   
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture', 'followers',"followers_count", "following_count"
            ]
    
    
class RegisterSerializer(serializers.ModelSerializer):
    """ serializers registering data """
    password = serializers.CharField(write_only=True)# must not be in the api we send

    class Meta:
        model = User
        fields = [
            "username", "email", "password"
        ]
    
    # overiding the user_creation_function
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
        username=validated_data["username"],
        email=validated_data["email"],
        password=validated_data["password"]
        )
        Token.objects.create(user=user)
        return user

    
class LoginSerializer(serializers.Serializer):
    """ serializers login credetial and validates """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
