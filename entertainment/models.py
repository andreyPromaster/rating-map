from django.contrib.gis.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Place(models.Model):
    name = models.CharField(max_length=255)
    location = models.PointField()
    address = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    CAFE = 'cafe'
    RESTAURANT = 'restaurant'
    SPORT = 'sport'
    TECH = 'tech'
    SHOP = 'shop'
    STUDY = 'study'
    TYPES_OF_PLACE = [
        (CAFE, 'Cafe'),
        (RESTAURANT, 'Restaurant'),
        (SPORT, 'Sport'),
        (TECH, 'Tech'),
        (SHOP, 'Shop'),
        (STUDY, 'Study'),
    ]
    type = models.CharField(
        max_length=20,
        choices=TYPES_OF_PLACE,
        default=CAFE,
    )


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    related_comments = models.ManyToManyField("self", symmetrical=False, blank=True)


class Rate(models.Model):
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateField(auto_now_add=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="ratings")
    user = models.OneToOneField(User, on_delete=models.SET(get_sentinel_user), related_name="user")
    comment = models.OneToOneField(Comment, on_delete=models.SET_NULL, null=True, blank=True)


