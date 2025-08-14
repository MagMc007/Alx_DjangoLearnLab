from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField
from django import forms
from .models import Post


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(
        label="Email_address",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
