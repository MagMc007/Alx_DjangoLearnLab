from django.contrib.auth.forms import UserChangeForm
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import (
    ListView, CreateView, DeleteView, DetailView, UpdateView
)
from .forms import PostForm


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


class PostListView(ListView):
    """ list all posts """
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    """ this one is for individual post access"""
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    """ for creating a post """
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("list-view")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ to update existing post"""
    model = Post
    form_class = PostForm
    # same template used for creating
    template_name = "blog/post_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user
    
    # for redirect upon completion of update
    def get_success_url(self):
        return reverse("detail-view", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ for deleting a post """
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("list-view")

    def test_func(self):
        return self.get_object().author == self.request.user
