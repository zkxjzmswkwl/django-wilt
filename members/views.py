from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Member
from .serializers import MemberSerializer
from .spot import *
import uuid
import requests


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    @action(detail=False, methods=["POST"])
    def register(self, request):
        if not request.user.is_anonymous:
            return Response({"err": "Can't make an account while logged in."})

        username = request.data.get("username", None)
        password = request.data.get("username", None)
        email = request.data.get("username", None)

        if email is None:
            email = f"balls{uuid.uuid4().hex[:24]}@gmail.com"

        new_member = Member(
                username=username, email=email)

        new_member.set_password(password)
        new_member.save()

        return Response(MemberSerializer(instance=new_member).data)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        if request.user.is_anonymous:
            return Response(data={"err": "You're not logged in men."})
        return Response(MemberSerializer(instance=request.user).data)

    @action(detail=False, methods=["GET"])
    def spotify_callback(self, request):
        auth_token = request.COOKIES.get("Authorization")
        user = Member.objects.get(id=Token.objects.get(key=auth_token).user_id)
        r = requests.post(
            "https://accounts.spotify.com/api/token",
            data = {
                "code": request.query_params.get("code"),
                "redirect_uri": "http://localhost:6969/pusherman/members/spotify_callback/",
                "grant_type": "authorization_code"
            },
            headers = {
                "Authorization": f"Basic {Morbify.encodeshit().decode('ascii')}"
            }
        )
        data = r.json()
        user.spotify_auth_code = data.get("access_token")
        user.spotify_refresh_code = data.get("refresh_token")
        user.save()

        Morbify.play(user.spotify_auth_code, ['spotify:track:0jPprFhDpOfkK3AmgYUCKg'])
        return Response({"nice": "Done :)"})

    @action(detail=False, methods=["GET"])
    def spotify_auth(self, request):
        s = "https://accounts.spotify.com/authorize"
        s += f"?client_id={client_id}&response_type=code"
        s += f"&redirect_uri=http://localhost:6969/pusherman/members/spotify_callback/"
        s += "&scope=user-read-currently-playing user-modify-playback-state"
        s += "&show_dialog=True"
        s += "&state=Carter"
        return HttpResponse(s)
    
    @action(detail=False, methods=["GET"])
    def spf_listening(self, request):
        import json
        return Response(json.loads(Morbify.get_currently_playing(request.user)))
