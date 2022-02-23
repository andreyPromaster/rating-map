from rest_framework import serializers

from entertainment.models import Place, Rate
from user.serializers import UserSerializer


class RateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rate
        fields = ("user", "rating", "created_at", "comment")


class PlaceSerializer(serializers.ModelSerializer):
    ratings = RateSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = ("id", "name", "location", "address", "image", "type", "ratings")