from api.models import Book, Author
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class API_Tests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Runs only once and does not go to default database
        """
        # created the authors
        cls.author1 = Author.objects.create(name="testauthor1")
        cls.author2 = Author.objects.create(name="testauthor2")

        # create books
        Book.objects.create(
            title="testbook1", 
            publication_year="2018",
            author=cls.author1
            )
        
        Book.objects.create(
            title="testbook2", 
            publication_year="2020",
            author=cls.author2
            )
            
    
    def test_create_book(self):
        data = {
            "title": "newbook",
            "publication_year": "2023",
            "author": self.author1.id
        }
