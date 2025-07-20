from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.decorators import login_required, user_passes_test

def list_books(request):
    """Obtains all books from databse and renders some html"""
    books = Book.objects.all()

    context = {"book_list": books}  #store it in context  as dynamic data

    return render(request, "relationship_app/list_books.html", context)


# Create your views here.
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = 'library'
    

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user) 
            return redirect("login") 
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html", {"form": form})

#decorator to check role
def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@login_required
@user_passes_test(is_admin, login_url='/relationship/login/')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian, login_url='/relationship/login/')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(is_member, login_url='/relationship/login/')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
