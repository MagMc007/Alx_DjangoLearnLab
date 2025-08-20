from django.db import models
# import the new user model form settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    """ post for a user """
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_by")
    

class Comment(models.Model):
    """ a comment on a post """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented_by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_on")
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")