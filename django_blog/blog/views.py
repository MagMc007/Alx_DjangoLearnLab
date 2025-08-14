from django.contrib.auth.forms import UserChangeForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .serializer import PostSerializer
from .models import Post


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

@login_required
def edit_profiles(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, "blog/change_profile.html", {
        "form": form,
    })


class ListView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class DetailView(generics.RetrieveAPIView):
    ...


class CreateView(generics.CreateAPIView):
    ...


class UpdateView(generics.UpdateAPIView):
    ...


class DeleteView(generics.DestroyAPIView):
    ...