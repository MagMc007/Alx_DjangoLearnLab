from .views import list_books, LibraryDetailView
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", LibraryDetailView.as_view(), name="funcDisplayDetail"),
    path("", list_books, name="classDisplayDetail"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]