from rest_framework.serializers import ModelSerializer
from .models import Member


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        exclude = ("password", "email")
