from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http.response import HttpResponse
from .datadl import gen_scrobble_sheet

from .models import Artist, Album, Song, Scrobble
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer, ScrobbleSerializer, ScrobbleSerializerVerbose


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = ArtistSerializer


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class ScrobbleViewSet(ModelViewSet):
    queryset = Scrobble.objects.all()
    serializer_class = ScrobbleSerializerVerbose

    @action(detail=False, methods=["POST"])
    def listen(self, request):
        if request.user.is_anonymous:
            return Response(data={"err": "Must be authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        artist = request.data.get("artist", None)
        song = request.data.get("song", None)

        if artist is None or song is None:
            return Response(data={"err": "artist and song both required fields."})
        
        # Check if the artist already exists in our db
        artist_obj, created = Artist.objects.get_or_create(title=artist)
        print(created)
        print(artist_obj)

        # Check if the song already exists in our db
        check_song = Song.objects.filter(title__iexact=song).exists()
        song_obj = None

        if check_song:
            song_obj = Song.objects.get(title__iexact=song)
            if song_obj.artist.title == artist:
                # Not the first time someone's listened to this song,
                # increment listen_count.
                song_obj.increment_listens()
        else:
            song_obj = Song.objects.create(title=song, artist=artist_obj)

        scrobble = Scrobble.objects.create(belongs_to=request.user, song=song_obj)
        return Response(ScrobbleSerializer(instance=scrobble).data)

    @action(detail=False, methods=["GET"])
    def by_artist(self, request):
        artist_id = request.query_params.get("id", None)
        if artist_id is None:
            return Response(data={"err": "required parameter id not found."})

        queryset = self.queryset.filter(song__artist__id=artist_id)
        return Response(ScrobbleSerializerVerbose(instance=queryset, many=True).data)

    @action(detail=False, methods=["GET"])
    def by_user(self, request):
        user_id = request.query_params.get("id", None)
        username = request.query_params.get("username", None)

        if user_id is None and username is None:
            return Response(data={"err": "must provide either username or id param."})

        if user_id is not None and username is not None:
            return Response(data={"err": "both username and id params received."})

        queryset = None

        if user_id is not None:
            queryset = self.queryset.filter(belongs_to__id=user_id)

        if username is not None:
            queryset = self.queryset.filter(belongs_to__username__iexact=username)
        
        return Response(ScrobbleSerializerVerbose(instance=queryset, many=True).data)

    @action(detail=False, methods=["GET"])
    def by_song(self, request):
        song_id = request.query_params.get("id", None)
        if song_id is None:
            return Response(data={"err": "required parameter id not found."})
        
        queryset = self.queryset.filter(song__id=song_id)
        return Response(ScrobbleSerializerVerbose(instance=queryset, many=True).data)

    @action(detail=False, methods=["GET"])
    def recent(self, request):
        count = request.query_params.get("count", None)
        if count is None:
            return Response(data={"err": "required parameter count not found."})

        queryset = self.queryset.order_by("-timestamp")[:int(count)]
        return Response(ScrobbleSerializerVerbose(instance=queryset, many=True).data)
    
    @action(detail=False, methods=["GET"])
    def dl_my_scrobbles(self, request):
        given_id = request.query_params.get("user_id", None)

        if request.user.is_anonymous and given_id is None:
            return Response(data={"err": "men u are not logged in"})

        user_id = given_id

        formatting = request.query_params.get("formatting", None)
        if formatting is None:
            formatting = "xls"

        if formatting == "xls":
            return HttpResponse(gen_scrobble_sheet(user_id), content_type="text/plain")

