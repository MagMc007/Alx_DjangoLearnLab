from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailField


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(
        label="Email_address",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)