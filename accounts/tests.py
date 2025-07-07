from django.test import TestCase
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user_model 

User = get_user_model()  # Use the custom user model if set in settings.py
class CustomuserModelTest(TestCase):

    def setUp(self):
        self.profile = CustomUser.objects.create_user(
            username='Valentine',
            email='val@test.com',
            password='password123'
        )
        self.profile.is_verified = True
        self.profile.verification_code = '123456'
        self.profile.save()

    def test_profile_created_correctly(self):
        self.assertEqual(self.profile.username, 'Valentine')
        self.assertEqual(self.profile.email, 'val@test.com')
        self.assertTrue(self.profile.is_verified)
        self.assertEqual(self.profile.verification_code, '123456')

    def test_profile_password(self):
        self.assertTrue(self.profile.check_password('password123'))  # ✅ fixed

    def test_profile_str_method(self):
        self.assertEqual(str(self.profile), 'Valentine')  # ✅ works if __str__ returns username

class AccountsViewTests(TestCase):

    def test_register_view_status_code(self):
        url = reverse('register')  # Replace with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')  # Adjust the template path

    def test_login_view_status_code(self):
        url = reverse('login')  # Replace with your actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')  # Adjust the template path

    def test_profile_view_status_code(self):
        user = User.objects.create_user(username='valentine', password='val3usiku')
        self.client.login(username='valentine', password='val3usiku')
        url = reverse('profile')