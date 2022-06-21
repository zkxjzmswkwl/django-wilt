from rest_framework.serializers import ModelSerializer, StringRelatedField, ReadOnlyField
from .models import Artist, Album, Song, Scrobble

# Woohoo, I love boilerplate!


# -------------------------
# Base(efficient) serializers


class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class SongSerializer(ModelSerializer):
    art = ReadOnlyField()

    class Meta:
        model = Song
        fields = "__all__"


class ScrobbleSerializer(ModelSerializer):
    class Meta:
        model = Scrobble
        fields = "__all__"


# -------------------------
# Based(lazy) serializers


class ScrobbleSerializerVerbose(ModelSerializer):
    song = StringRelatedField()
    artist = ReadOnlyField()
    belongs_to = StringRelatedField()
    art = ReadOnlyField()

    class Meta:
        model = Scrobble
        fields = "__all__"


class SongSerializerVerbose(ModelSerializer):
    artist = ReadOnlyField()

