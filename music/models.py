from django.db import models


class Artist(models.Model):
    title = models.CharField(max_length=124, unique=True, blank=False, null=False)
    active = models.BooleanField(default=True)
    year = models.DateTimeField(null=True, blank=True)
    year_disband = models.DateTimeField(null=True, blank=True)
    formed_in = models.CharField(max_length=82, null=True, blank=True)
    about = models.TextField(max_length=4800, null=True, blank=True)
    pic = models.FileField(upload_to="artists/", null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id})"


class Album(models.Model):
    title = models.CharField(max_length=124, unique=True, blank=False, null=False)
    year = models.DateTimeField(null=True, blank=True)
    cover = models.FileField(upload_to="covers/", null=True, blank=True)
    about = models.TextField(max_length=4800, null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id})"



class Song(models.Model):
    title = models.CharField(max_length=124, unique=True, blank=False, null=False)
    year = models.DateTimeField(null=True, blank=True)
    about = models.TextField(max_length=2800, null=True, blank=True)
    """
    While it'd be nice to just use the song's album__artist field to get a link back to the artist,
    not every song will have an album, some songs are leaked/released post-mortem etc etc.
    So we store both.

    ---

    We can surmise the artist's total listen count from querying all their songs.
    Same with albums.
    Nothing necessary when it comes to songs that are album-less. Little orphan songs.
    """
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    """"""
    listen_count = models.IntegerField(default=0)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id})"


