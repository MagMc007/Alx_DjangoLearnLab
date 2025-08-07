from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin,
    DestroyModelMixin, UpdateModelMixin
)


""" this will list existing books """
class ListView(GenericAPIView, ListModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


""" this will retrieve a singe books by id """
class DetailView(GenericAPIView, RetrieveModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

""" this will allow creating of a book """
class CreateView(GenericAPIView, CreateModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


""" this update an existing book """
class UpdateView(GenericAPIView, UpdateModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


""" this will delete an existing book """
class DeleteView(GenericAPIView, DestroyModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
