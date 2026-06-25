from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Manager that uses email as the unique identifier."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model — email is the unique identifier, username is removed."""

    username = None
    groups = None
    user_permissions = None
    email = models.EmailField(unique=True, max_length=254)
    full_name = models.CharField(max_length=150)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.email


class LoginAttempt(models.Model):
    """Records each login attempt. Lockout: >= 3 failures in 2 hours."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="login_attempts"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()

    def __str__(self):
        status = "OK" if self.success else "FAIL"
        return f"{self.user.email} — {status} @ {self.timestamp}"


class UserSession(models.Model):
    """Enforces one active session per user (OneToOne)."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="active_session"
    )
    session_key = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.user.email} → session {self.session_key[:8]}..."
