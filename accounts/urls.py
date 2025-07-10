from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .forms import SmartAuthForm


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html',authentication_form=SmartAuthForm)),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.CustomPasswordChangeView.as_view(template_name='accounts/change_password.html'
    ), name='password_change'),
    path('verify/', views.verify_user, name='verify_user'),
    path('home/', views.home, name='home'),
] 