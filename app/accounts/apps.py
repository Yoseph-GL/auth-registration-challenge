from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Conecto las señales para que Django ejecute el handler cuando el usuario inicia sesión
        import accounts.signals  # noqa: F401
