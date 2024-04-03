from django.db import models
from members.models import Member


class Artist(models.Model):
    title = models.CharField(max_length=124, unique=True, blank=False, null=False)
    active = models.BooleanField(default=True)
    year = models.DateTimeField(null=True, blank=True)
    year_disband = models.DateTimeField(null=True, blank=True)
    formed_in = models.CharField(max_length=82, null=True, blank=True)
    about = models.TextField(max_length=4800, null=True, blank=True)
    pic = models.FileField(upload_to="artists/", null=False, blank=False, default="artists/Cover.jpg")
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def photo(self):
        check = Album.objects.filter(artist=self)
        if check.exists():
            if check.first().cover:
                return check.first().cover.url


class Album(models.Model):
    title = models.CharField(max_length=124, blank=False, null=False)
    year = models.DateTimeField(null=True, blank=True)
    cover = models.FileField(upload_to="covers/", null=True, blank=True)
    about = models.TextField(max_length=4800, null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id})"


class Song(models.Model):
    title = models.CharField(max_length=124, blank=False, null=False)
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

    listen_count = models.IntegerField(default=1)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def increment_listens(self):
        self.listen_count = self.listen_count + 1
        self.save()

    #  @property
    #  def artist(self):
        #  """
        #  maybe stupid decision from stupid man ook ook.
        #  we already have this on Scrobble, so it might be worth
        #  just leaving this here, then removing the property from Scrobble
        #  in favor of this 'un here.
        #  """
        #  return self.artist.title


class Scrobble(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.song.title} - {self.member.username}"

    # TODO: See line 55
    @property
    def art(self):
        if self.song.artist.pic.name:
            return self.song.artist.pic.url
        return "None"

    @property
    def artist(self):
        return self.song.artist.title

    @property
    def spreadsheet_entry(self):
        return f"{self.timestamp},{self.song.artist.title},{self.song.title}"

