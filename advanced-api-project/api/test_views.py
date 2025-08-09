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
        Book.objects.create(
            title="testbook3", 
            publication_year="1900",
            author=cls.author2
            )
            
    def test_filter_book_by_publication_year(self):
        """
        Tests filtering based on publication year of the book
        """

        # prepare the url route of filter
        # GET /books/?publication_year=2020 must return just one book
        url = reverse("list-view") + "?publication_year=2020"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        """ 
        Test seraching a book by title 
        """
        # prepare url 
        # GET /books/?search=the_book_title
        url = reverse("list-view") + "?title=testbook3"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "testbook3")
    
    def test_ordering_book_by_title_asc(self):
        """
        tests ordering by title in ascending order
        """
        url = reverse('list-view')
        response = self.client.get(url + '?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Verify the first book 
        self.assertEqual(response.data[0]['title'], 'testbook1')
    
    def test_unauthenticated_user_cannot_create_book(self):
        """
        Test that unauthenticated users receive a 401 error when creating a book.
        """
        url = reverse('create-view') 
        book_data = {
            'title': 'Unauths Book',
            'author': self.author1.id,
            'publication_year': 2024
        }
        response = self.client.post(url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_user_can_create_book(self):
        """
        Test that an authenticated user can successfully create a book.
        """
        # Authenticate the user
        self.client.login(username='testuser123', password='testpassword123')
        
        url = reverse('book-create') # Assumes URL is named in urls.py
        book_data = {
            'title': 'Auth users book',
            'author': self.author1.id,
            'publication_year': 2024
        }
        response = self.client.post(url, book_data, format='json')
        
        # Verify successful creation with 201 status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Confirm the book exists in the database
        self.assertTrue(Book.objects.filter(title='Auth users book').exists())