from django.contrib.gis.measure import D
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.contrib.gis.geos import Point
from entertainment.models import Place
from entertainment.serializers import PlaceSerializer


@api_view(['GET'])
def ping(request):
    return Response({"text": "pong"})


class PlaceListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)

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


