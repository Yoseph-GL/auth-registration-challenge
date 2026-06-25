from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Conectar las señales para que Django ejecute el handler al iniciar sesión
        # El import vacío es a propósito: al cargar el módulo se registran los @receiver
        import accounts.signals  # noqa: F401
