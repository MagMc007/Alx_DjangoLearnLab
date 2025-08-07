from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

""" handle serializing of the book model with valisation"""


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    """ check if pub_yr is not from the future and raise error """
    def validate_publication_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError("{'publication_year': 'Cannot be from the future'}")
        return value

""" serialzes the Author model """
""" nest the book serializer to avoid extra query for a book"""


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["name", "books"]