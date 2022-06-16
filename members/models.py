from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token


class Member(AbstractBaseUser):
    """
    Just need representation of the user model, even though we're extending Django's.
    Enables additions later down the line with less headache.
    """
    pass


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
