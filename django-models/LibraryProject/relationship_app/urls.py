from . import views
from django.urls import path

urlpatterns = [
    path("", views.DisplayDetails, name="funcDisplayDetail"),
    path("", views.listBooks, name="classDisplayDetail"),
]