from django.urls import path

from . import views
from .views import PlaceListAPIView, RelatedCommentAPIView

urlpatterns = [
    path("ping", views.ping, name="index"),
    path("places", PlaceListAPIView.as_view({"get": "list", "post": "create"}), name="place-list"),
    path("places/<int:pk>/ratings", PlaceListAPIView.as_view({"post": "create_rating"}), name="comment-list"),
    path("comments/<int:pk>/releted-comments", RelatedCommentAPIView.as_view({"post": "create_related_comment"}), name="related-comments")
]