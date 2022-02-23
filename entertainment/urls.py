from django.urls import path

from . import views
from .views import PlaceListAPIView

urlpatterns = [
    path("ping", views.ping, name="index"),
    path("places", PlaceListAPIView.as_view(), name="place-list")
]