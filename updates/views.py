from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Update
from .serializers import UpdateSerializer


class UpdateViewSet(ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer

