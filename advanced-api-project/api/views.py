from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter


""" this will list existing books """


class ListView(GenericAPIView, ListModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    """ to apply filterings like search, order and literal filters"""
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]
    """ the fields needed to filter"""
    filterset_fields = ["title", "author__name", "publication_year"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


""" this will retrieve a singe books by id """


class DetailView(GenericAPIView, RetrieveModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


""" this will allow creating of a book """


class CreateView(GenericAPIView, CreateModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


""" this update an existing book """


class UpdateView(GenericAPIView, UpdateModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


""" this will delete an existing book """


class DeleteView(GenericAPIView, DestroyModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
