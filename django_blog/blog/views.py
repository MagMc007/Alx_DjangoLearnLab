from django.contrib.auth.forms import UserChangeForm
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from django.views.generic import (
    ListView, CreateView, DeleteView, DetailView, UpdateView
)
from .forms import PostForm, CommentForm
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add comments for this post
        context["comments"] = Comment.objects.filter(post=self.object).order_by("created_at")
        return context


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    """ for creating comments """
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    # validate form and tie it to a post
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("detail-view", kwargs={"pk": self.kwargs["pk"]})


class CommentListView(ListView):
    """ lists all comments below the deatil view """
    model = Comment
    template_name = "blog/post_detail.html"
    context_object_name = "comments"
    
    # filter all comments tied to a post
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["pk"])
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """ update a comment for a post """
    model = Comment
    template_name = "blog/comment_form.html"
    form_class = CommentForm

    def test_func(self):
        # Only allow the author to update
        comment = self.get_object()
        return comment.author == self.request.user
    
    def get_success_url(self):
        comment = Comment.objects.get(pk=self.object.pk) 
        return reverse("detail-view", kwargs={"pk": comment.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ this one is for deleting a comment """
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        # Only the author can delete
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        # Redirect to the post detail page after deletion
        return reverse("detail-view", kwargs={"pk": self.object.post.pk})


def post_search(request):
    """ implements search functionality """
    query = request.GET.get("q")
    posts = Post.objects.all()

    if query:
        # filter by the required fields
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    return render(request, "blog/search_results.html", {"posts": posts, "query": query})