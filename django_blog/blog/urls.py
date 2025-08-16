from django.urls import path
from . import views 


urlpatterns = [
    path("register/", views.Registration.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("profile/", views.profile, name="home"),
    path("edit_profile/", views.edit_profiles, name="edit_profile"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("posts/", views.PostListView.as_view(), name="list-view"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="detail-view"),
    path("posts/new/", views.PostCreateView.as_view(), name="create-view"),
    path("posts/<int:pk>/update/", views.PostUpdateView.as_view(), name="update-view"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete-view"),
    path("posts/<int:pk>/comments/", views.CommentListView.as_view(), name="comment-list-view"),
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create-view"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update-view"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete-view"),
    path("search/", views.post_search, name="post-search"),
    path("tags/<slug:tag_slug>/", views.PostByTagListView.as_view(), name="posts-by-tag"),
]