from .views import list_books, LibraryDetailView, register
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", LibraryDetailView.as_view(), name="funcDisplayDetail"),
    path("", list_books, name="classDisplayDetail"),
    path('login/', LoginView.as_view(
        template_name='relationship_app/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(
        template_name='relationship_app/logout.html'), 
        name='logout'),
    path('register/', register, name='register'),
]