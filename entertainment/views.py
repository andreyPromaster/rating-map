from django.contrib.gis.measure import D
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework import generics, mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated

from django.contrib.gis.geos import Point
from entertainment.models import Place, Rate, Comment
from entertainment.serializers import PlaceSerializer, RateSerializer, CommentSerializer


@api_view(['GET'])
def ping(request):
    return Response({"text": "pong"})


class PlaceListAPIView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        photo = self.request.data['photo']
        serializer.save(image=photo)

    def filter_queryset(self, queryset):
        if ("longitude" in self.request.query_params
            and "latitude" in self.request.query_params):
            point = Point(float(self.request.query_params["longitude"]),
                          float(self.request.query_params["latitude"]),
                          srid=4326)
            queryset = queryset.filter(location__distance_lt =(point, D(km=2)))
        return queryset

    @action(detail=True, methods=['post'])
    def create_rating(self, request, pk=None):
        place = self.get_object()
        user = self.request.user
        serializer = RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Rate.objects.filter(user=user, place=place):
            raise ValidationError({"message": "User can create comment only ones"})

        comment_data = serializer.validated_data.pop('comment', None)
        if comment_data:
            comment = Comment.objects.create(text=comment_data["text"], user=user)
        else:
            comment = None
        rate = Rate(**serializer.validated_data, place=place, user=user, comment=comment)
        rate.save()
        return Response({"message": "Rate was created"}, status=status.HTTP_201_CREATED)


class RelatedCommentAPIView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Comment.objects.all()
    serializer_class = RateSerializer

    @action(detail=True, methods=['post'])
    def create_related_comment(self, request, pk=None):
        comment = self.get_object()
        user = self.request.user
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        related_comment = Comment.objects.create(text=serializer.validated_data["text"], user=user)
        comment.related_comments.add(related_comment)
        return Response({"id": related_comment.id,
                         "created_at": related_comment.created_at,
                         "text": serializer.validated_data["text"],
                         "username": user.username},
                        status=status.HTTP_201_CREATED)





