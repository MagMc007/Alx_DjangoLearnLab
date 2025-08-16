from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField
from django import forms
from .models import Post, Comment
from taggit.forms import TagField, TagWidget


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(
        label="Email_address",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
    

class PostForm(forms.ModelForm):
    tag = TagField(widget=TagWidget())
    
    class Meta:
        model = Post
        fields = ["title", "content", "tag"]
        widgets = {
            "tags": TagWidget(),  
            }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content",]