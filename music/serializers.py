from rest_framework.serializers import ModelSerializer
from .models import Artist, Album, Song

# Woohoo, I love boilerplate!


class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class AlbumSerializer(ModelSerializer):
    class Meta:
        model = Album
        fields = "__all__"


class SongSerializer(ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"

