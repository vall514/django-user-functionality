from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

   # or whatever you named it

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]   # add first_name, last_name, etc. if needed
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "email@example.com"}),
        }

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile                 # or User if you stored image there
        fields = ["image"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class SmartAuthForm(AuthenticationForm):
    """Adds a helpful error if the username doesn’t exist."""
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Username"}),
    )

    def clean(self):
        """
        If the username isn’t in the DB, short‑circuit normal auth and
        raise our own error message.
        """
        cleaned_data = super().clean()          # ← runs the normal auth logic
        username = self.cleaned_data.get("username")

        if username and not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "We couldn’t find an account called “%s”.  "
                "Would you like to <a href=\"%s\">create one</a>?" %
                (username, reverse("register")),
                code="unknown_user",
                params={"username": username},
            )

        # If the user exists but the password is wrong, the parent class
        # has already attached its usual “Please enter a correct username
        # and password” error, so we just return.
        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']