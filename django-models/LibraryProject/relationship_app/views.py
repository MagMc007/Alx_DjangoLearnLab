from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library


def listBooks(request):
    """Obtains all books from databse and renders some html"""
    books = Book.objects.all()

    context = {"book_list": books}  #store it in context  as dynamic data

    return render(request, "relationship_app/list_books.html", context)


# Create your views here.
class DisplayDetails(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = 'library'
    

