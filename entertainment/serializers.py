from django.contrib.gis.geos import Point
from rest_framework import serializers

from entertainment.models import Place, Rate, Comment
from user.serializers import UserSerializer


class RelatedCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", required=False)

    class Meta:
        model = Comment
        fields = ("id", "created_at", "text", "username")
        read_only_fields = ("username", )


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", required=False)
    related_comments = RelatedCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "created_at", "text", "related_comments", "username")
        read_only_fields = ("related_comments", "username")


class RateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    comment = CommentSerializer(required=False)

    class Meta:
        model = Rate
        fields = ("user", "rating", "created_at", "comment")


class PlaceSerializer(serializers.ModelSerializer):
    ratings = RateSerializer(many=True, read_only=True)
    longitude = serializers.CharField(source="location.x")
    latitude = serializers.CharField(source="location.y")

    class Meta:
        model = Place
        fields = ("id", "name", "longitude", "latitude", "address", "image", "type", "ratings")

    def create(self, validated_data):
        location = Point(
            float(validated_data.get("location").get('x')),
            float(validated_data.get("location").get('y')),
            srid=4326
        )
        validated_data.pop("location")
        return Place.objects.create(location=location, **validated_data)