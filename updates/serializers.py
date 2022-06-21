from rest_framework.serializers import ModelSerializer
from .models import Update


class UpdateSerializer(ModelSerializer):

    class Meta:
        model = Update
        fields = "__all__"

