from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'), ('Librarian', 'Librarian'), ('Member', 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user} with {self.role}"


class Author(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name="books"
        )
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
    
    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=20)
    books = models.ManyToManyField(
        Book,
        related_name="library"
    )

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=20)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name="librarian"
    )

    def __str__(self):
        return self.name
