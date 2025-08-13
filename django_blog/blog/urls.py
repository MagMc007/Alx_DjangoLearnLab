from django.urls import path
from .views import Registration, LoginUser, profile, LogoutUser

urlpatterns = [
    path("register/", Registration.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("profile/", profile, name="home"),
    path("logout/", LogoutUser.as_view(), name="logout")
]