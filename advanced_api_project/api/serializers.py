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
            raise serializers.ValidationError("A book from the future")
        return value

""" serialzes the Author model """


class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ["name", "book", ]