from rest_framework.serializers import ModelSerializer, StringRelatedField, ReadOnlyField, Serializer, SerializerMethodField
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
    member = StringRelatedField()
    art = SerializerMethodField()

    def get_art(self, obj):
        if obj.song.album.cover:
            return obj.song.album.cover.url

    class Meta:
        model = Scrobble
        fields = "__all__"


class ArtistSerializerVerbose(ModelSerializer):
    photo = SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo

    class Meta:
        model = Artist
        fields = "__all__"


class SongSerializerVerbose(ModelSerializer):
    album_photo = SerializerMethodField()

    def get_album_photo(self, obj):
        if obj.album.cover:
            return obj.album.cover.url
    
    class Meta:
        model = Song
        fields = "__all__"
