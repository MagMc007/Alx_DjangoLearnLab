from django.shortcuts import render
from django.views.genric import DetailView
from .models import Book


def listBooks(request):
    """Obtains all books from databse and renders some html"""
    books = Book.object.all()

    context = {"book_list": books}  #store it in context  as dynamic data

    return render(request, "list_books.html", context)


# Create your views here.
class DisplayDetails(DetailView):
    model = Book
    template_name = "library_detail.html"
    context_object_name = 'library'
    

