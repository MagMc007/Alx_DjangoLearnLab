from django.shortcuts import render
from django.views.genric import DetailView
from .models import Books


def listBooks(request):
    """Obtains all books from databse and renders some html"""
    books = Books.object.all()

    context = {"book_list": books}  #store it in context  as dynamic data

    return render(request, "relationhip_app/templates/list_books.html", context)


# Create your views here.
class DisplayDetails(DetailView):
    

