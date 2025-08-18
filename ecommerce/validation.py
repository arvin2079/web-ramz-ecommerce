from django.core.exceptions import ValidationError


def validate_half_or_whole(value):
    """
    Validator for ratings that allows only whole numbers (e.g. 1, 2, 3)
    or half-step increments (e.g. 1.5, 2.5, 3.5).
    Rejects values like 2.3, 4.7, etc.
    """
    if value * 2 != int(value * 2):
        raise ValidationError(
            f"{value} is not valid. Rating must be a whole number or end with .5."
        )