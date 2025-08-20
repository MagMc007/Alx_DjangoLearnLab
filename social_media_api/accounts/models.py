from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ custom user with additional fields """
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    followering = models.ManyToManyField("self", symmetrical=False, related_name="followed_by", blank=True)
