from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Member
from .serializers import MemberSerializer


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    @action(detail=False, methods=["GET"])
    def me(self, request):
        if request.user.is_anonymous:
            return Response(data={"err": "You're not logged in men."})
        return Response(MemberSerializer(instance=request.user).data)

