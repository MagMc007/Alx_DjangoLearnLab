from django.urls import path
from . import views 


urlpatterns = [
    path("register/", views.Registration.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("profile/", views.profile, name="home"),
    path("edit_profile/", views.edit_profiles, name="edit_profile"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("post/", views.PostListView.as_view(), name="list-view"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="detail-view"),
    path("post/new/", views.PostCreateView.as_view(), name="create-view"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="update-view"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete-view"),
]