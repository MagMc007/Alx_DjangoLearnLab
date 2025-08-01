from .serializers import BookSerializer
from rest_framework import generics, viewsets
from .models import Book
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]