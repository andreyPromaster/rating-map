from django.contrib.gis.db import models

from django.contrib.auth import get_user_model

from entertainment.validators import validate_rating

User = get_user_model()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Place(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()
    address = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    type = models.CharField(
        max_length=200,
        default="shop",
    )


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    related_comments = models.ManyToManyField("self", symmetrical=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="users_comment")

    class Meta:
        ordering = ['created_at']


class Rate(models.Model):
    rating = models.PositiveSmallIntegerField(validators=[validate_rating,])
    created_at = models.DateTimeField(auto_now_add=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="user")
    comment = models.OneToOneField(Comment, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ["place", "user"]
        ordering = ['-created_at']
