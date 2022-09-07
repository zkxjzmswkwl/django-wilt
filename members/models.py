from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class Member(AbstractUser):
    """
    Just need representation of the user model, even though we're extending Django's.
    Enables additions later down the line with less headache.
    """
    spotify_auth_code = models.CharField(max_length=250, default="None")
    spotify_refresh_code = models.CharField(max_length=250, default="None")

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

