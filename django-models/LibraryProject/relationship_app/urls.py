from .views import list_books, LibraryDetailView
from django.urls import path

urlpatterns = [
    path("", DisplayDetails, name="funcDisplayDetail"),
    path("", list_books, name="classDisplayDetail"),
]