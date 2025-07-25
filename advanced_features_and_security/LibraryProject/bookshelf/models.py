from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .forms import ExampleForm


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return (
            f"Title: {self.title} by {self.author} publsihed in {self.publication_year}"
        )


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extrafields):
        if not username:
            raise ValueError("User needs a username")
        email = self.normalize_email(email)

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username, email, full_name, password=None, **extrafields
    ):
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extrafields)


"""Custom user class for creating custom user"""


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to="profile_photos/", null=True, blank=True
    )

    objects = CustomUserManager

    def __str__(self):
        return self.username


"""Custom Permission for users"""


class CustomPermission(models.Model):
    class Meta:
        permissions = [
            ("can_view", "Can View"),
            ("can_create", "Can create"),
            ("can_edit", "Can Edit"),
            ("can_delete", "Can delete"),
        ]

        
def search_view(request):
    form = ExampleForm(request.GET)