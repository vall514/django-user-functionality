# accounts/models.py
from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# ---------- 1. Custom user model ----------
class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.username


# ---------- 2. Profile model ----------
def user_avatar_path(instance, filename):
    """
    Files will be uploaded to:
       MEDIA_ROOT / profile_pics / <username> / <filename>
    """
    return Path("profile_pics") / instance.user.username / filename


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # points to CustomUser
        on_delete=models.CASCADE,
        related_name="profile",
    )
    image = models.ImageField(
        upload_to=user_avatar_path,
        default="profile_pics/default-avatar.png",
    )

    def __str__(self):
        return f"{self.user.username} Profile"


# ---------- 3. Signals to manage Profile ----------
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    • When a new user is created → create linked Profile
    • When a user is saved → save the Profile as well
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
