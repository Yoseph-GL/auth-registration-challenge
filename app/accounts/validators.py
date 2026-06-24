import re

from django.core.exceptions import ValidationError


def validate_password_strength(password):
    """US01 AC03: at least 8 chars, one letter, and one number."""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r"[A-Za-z]", password):
        raise ValidationError("Password must contain at least one letter.")

    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one number.")
