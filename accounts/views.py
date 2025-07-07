from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Change this if you add login view later
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def profile_view(request):
    return render(request, 'accounts/profile.html')

def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})