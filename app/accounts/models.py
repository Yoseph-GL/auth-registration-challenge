from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    # Definir el email como campo único para autenticar en lugar del username

    def create_user(self, email, password=None, **extra_fields):
        # Pasar email a minúsculas y hashear password antes de guardar
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Forzar permisos de admin para que createsuperuser funcione sin pedirlos
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # Heredar de AbstractUser y eliminar username para que el login sea solo con email

    # Anular estos campos con None para que Django no los cree como columnas
    username = None
    first_name = None
    last_name = None
    groups = None
    user_permissions = None
    email = models.EmailField(unique=True, max_length=254)
    full_name = models.CharField(max_length=150)

    # USERNAME_FIELD: campo que identifica al usuario; REQUIRED_FIELDS: campos extra que pide createsuperuser
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.email


class LoginAttempt(models.Model):
    # Guardar cada intento de login para bloquear la cuenta tras 3 fallos en 2 horas

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="login_attempts"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()

    def __str__(self):
        status = "OK" if self.success else "FAIL"
        return f"{self.user.email} -- {status} @ {self.timestamp}"


class UserSession(models.Model):
    # Usar OneToOneField para que cada usuario solo tenga una sesión activa

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="active_session"
    )
    # Las session keys de Django miden 32 chars; 40 da margen por si cambia el backend
    session_key = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.user.email} → session {self.session_key[:8]}..."
