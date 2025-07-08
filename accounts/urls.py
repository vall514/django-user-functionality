from django.urls import path
from .import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.CustomPasswordChangeView.as_view(template_name='accounts/change_password.html'
    ), name='change_password'),
    path('verify/', views.verify_user, name='verify_user'),
    path('home/', views.profile_view, name='home')
] 