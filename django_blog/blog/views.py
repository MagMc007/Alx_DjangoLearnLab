from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
#from .forms import CustomUserCreationForm


class Registration(CreateView):
    form_class = UserCreationForm
    # success_url = reverse_lazy()
    template_name = "blog/register.html"