#from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class Registration(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "blog/register.html"


class LoginUser(LoginView):
    template_name = "blog/login.html"
    next_page = reverse_lazy("home")


@login_required
def profile(request):
    return render(request, "blog/profile.html")


class LogoutUser(LogoutView):
    template_name = "blog/logout.html"
    next_page = reverse_lazy("login")