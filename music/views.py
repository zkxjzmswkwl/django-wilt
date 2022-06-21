from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http.response import HttpResponse

import uuid

from .datadl import gen_scrobble_sheet

from .models import Artist, Album, Song, Scrobble
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer, ScrobbleSerializer, ScrobbleSerializerVerbose


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    @action(detail=True, methods=["GET"])
    def get_top_songs(self, request, pk=None):
        """
        Gets the most listened to songs for an artist.
        By default, it returns an ordered count of 10.
        
        To overwrite the default countm, specify ?count=<int> 
        """
        if pk is None:
            return Response({"err": "required parameter /artists/:id not found."}, status=status.HTTP_400_BAD_REQUEST)

        # TODO: Someone please tell me if there's a way to, in one call, get and cast a value from a dict.
        # I feel like there definitely is?
        count = request.query_params.get("count", None)
        if count is None:
            count = 10
        else:
            # If a count was specified via ?count, it will be of type str.
            # We need it to be type int in order to call [:int]
            count = int(count)

        songs = Song.objects.filter(artist__id=int(pk)).order_by("-listen_count")[:count]
        return Response(SongSerializer(instance=songs, many=True).data)

    @action(detail=False, methods=["POST"])
    def upload_art(self, request):
        artist_name = request.query_params.get("artist", None)
        if artist_name is None:
            return Response(data={"err": "required param artist not found."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = request.data.get("file", None)
        if uploaded_file is None:
            return Response({"err": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        print(uploaded_file.name)
        uploaded_file.name = f"{uuid.uuid4().hex[:32]}.jpg"

        artist = Artist.objects.get(title__iexact=artist_name)
        artist.pic = uploaded_file
        artist.save()
        return HttpResponse("aiosjdasd")

    @action(detail=False, methods=["GET"])
    def get_by(self, request):
        queryset = None
        name = request.query_params.get("name", None)
        if name is not None:
            queryset = self.queryset.get(title__iexact=name)
        return Response(ArtistSerializer(instance=queryset).data)
    
    @action(detail=True, methods=["GET"])
    def top_listeners(self, request, pk=None):
        if pk is None:
            return Response(data={"err": "pk is none"}, status=status.HTTP_400_BAD_REQUEST)
        # TODO: Come back to this when final db schema decisions made.
        pass

    @action(detail=True, methods=["GET"])
    def count(self, request, pk=None):
        if pk is None:
            return Response(data={"err": "pk is none"}, status=status.HTTP_400_BAD_REQUEST)

        artist = Artist.objects.get(id=pk)
        scrobble_count = Scrobble.objects.all().filter(
                song__artist__title__iexact=artist.title).count()
        return Response({"count": scrobble_count})
    
    @action(detail=True, methods=["GET"])
    def recent_listens(self, request, pk=None):
        if pk is None:
            return Response(data={"err": "pk is none"}, status=status.HTTP_400_BAD_REQUEST)

        count = request.query_params.get("count", 4)
        artist = Artist.objects.get(id=pk)
        recent_scrobbles = Scrobble.objects.all().filter(
                song__artist__title__iexact=artist.title).order_by("-timestamp")[:int(count)]
        return Response(ScrobbleSerializerVerbose(instance=recent_scrobbles, many=True).data)



class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


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

        if "encodeplussymbol" in artist:
            artist.replace("encodeplussymbol", "+")
        
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

