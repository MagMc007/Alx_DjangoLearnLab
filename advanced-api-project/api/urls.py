from django.urls import path
from .views import ListView, CreateView, DeleteView, DetailView, UpdateView

urlpatterns = [
    path("books/", ListView.as_view(), name="list-view"),
    path("books/create/", CreateView.as_view(), name="create-view"),
    path("books/<int:pk>/", DetailView.as_view(), name="detail-view"),
    path("books/delete/<int:pk>/", DeleteView.as_view(), name="delete-view"),
    path("books/update/<int:pk>/", UpdateView.as_view(), name="update-view"),
]