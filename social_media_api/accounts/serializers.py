from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """ serializes only user info """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']
    
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
        user = User.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user

    
class LoginSerializer(serializers.Serializers):
    """ serializers login credetial and validates """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(usename=data["username"], password=["password"])
        if user and user.is_active():
            return user
        raise serializers.ValidationError("Invalid credentials")
