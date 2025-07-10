from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random
from .forms import EditProfileForm ,CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditProfileForm, ProfileImageForm   # new form for the image
from .models import Profile                             # if you use a separate model


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')  # R




User = get_user_model()
from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

# accounts/views.py# Make sure to import your Profile model

@login_required
def profile_view(request):
    # Get or create profile - this fixes the error
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        image_form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and image_form.is_valid():
            user_form.save()
            image_form.save()
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        image_form = ProfileImageForm(instance=profile)
     
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'image_form': image_form
    })
@login_required
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        user_form  = EditProfileForm(request.POST, instance=user)
        image_form = ProfileImageForm(
            request.POST, request.FILES, instance=profile
        )
        if user_form.is_valid() and image_form.is_valid():
            user_form.save()
            if request.FILES.get("image"):
                image_form.save()
            messages.success(request, "Profile updated!")
            return redirect("profile")
    else:
        user_form  = EditProfileForm(instance=user)
        image_form = ProfileImageForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {"user_form": user_form, "image_form": image_form},
    )



def verify_user(request):
    username = request.session.get('username_to_verify')
    if not username:
        return redirect('login')

    user = User.objects.get(username=username)

    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.verification_code:
            user.is_verified = True
            user.save()
            del request.session['username_to_verify']
            return redirect('login')  # or profile
        else:
            return render(request, 'accounts/verify.html', {'error': 'Invalid verification code'})

    return render(request, 'accounts/verify.html')

def home(request):
    return render(request, 'accounts/home.html')
