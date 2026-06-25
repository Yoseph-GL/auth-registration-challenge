import re

from django.core.exceptions import ValidationError


class PasswordStrengthValidator:
    """US01 AC03: at least 8 chars, one letter, and one number."""

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long."
            )
        if not re.search(r"[A-Za-z]", password):
            raise ValidationError(
                "Password must contain at least one letter."
            )
        if not re.search(r"[0-9]", password):
            raise ValidationError(
                "Password must contain at least one number."
            )

    def get_help_text(self):
        return (
            "Your password must be at least 8 characters long "
            "and contain at least one letter and one number."
        )
