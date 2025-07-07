from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random
from.forms import EditProfileForm
from django.contrib import messages




User = get_user_model()
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.verification_code = str(random.randint(100000, 999999))
            user.save()
            print(f"Mock verification code for {user.username}: {user.verification_code}")
            request.session['username_to_verify'] = user.username
            return redirect('verify_user')
        else:
            print(form.errors)  # 🔍 Print form errors in the console
            messages.error(request, "Please correct the errors below.")  # Show error message
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})
 

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('verify_user')  # Redirect to login if user is not authenticated  
    return render(request, 'accounts/profile.html')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


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