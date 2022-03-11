from django.core.exceptions import ValidationError


def validate_rating(value):
    if value < 0 or value > 5:
        raise ValidationError("Rating must be in [0, 5]")
