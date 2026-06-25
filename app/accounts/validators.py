import re

from django.core.exceptions import ValidationError


class PasswordStrengthValidator:
    # Exigir mínimo 8 caracteres, al menos una letra y un número

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
        # Mostrar las reglas de la contraseña como ayuda en el formulario
        return (
            "Your password must be at least 8 characters long "
            "and contain at least one letter and one number."
        )
