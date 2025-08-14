from django.urls import path
from . import views 


urlpatterns = [
    path("register/", views.Registration.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("profile/", views.profile, name="home"),
    path("edit_profile/", views.edit_profiles, name="edit_profile"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("post/", views.ListView.as_view(), name="list-view"),
    path("post/new/", views.CreateView.as_view(), name="list-view"),
    path("post/<int:pk>", views.DetailView.as_view(), nama="detail-view"),
    path("post/<int:pk>/edit", views.UpdateView.as_view(), name="update-view"),
    path("post/<int:pk>/delete", views.DeleteView.as_view(), name="delete-view"),
]