from django.contrib import admin

from django.contrib.gis.admin import OSMGeoAdmin
from .models import Place, Rate, Comment


@admin.register(Place)
class PlaceAdmin(OSMGeoAdmin):
    list_display = ('name', 'location', 'address', 'image', 'type')


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("rating", "created_at", "user", "comment")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at",)