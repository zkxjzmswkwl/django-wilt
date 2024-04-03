from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from .models import Album
import music.musicbrainz as mb

@receiver(post_save, sender=Album)
def download_and_set_album_cover(sender, instance, created, **kwargs):
    if created:
        mb.download_album_cover(instance)