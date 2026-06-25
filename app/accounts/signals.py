from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import UserSession


@receiver(user_logged_in)
def enforce_single_session(sender, request, user, **kwargs):
    """US02 AC12: ensure only one active session per user.

    Deletes any previous UserSession for this user. The OneToOneField
    guarantees only one session is tracked at a time. We do NOT delete
    django_session rows — Django manages session expiry on its own, and
    touching them can cause SessionInterrupted when the same user logs
    in again without a session key rotation.
    """
    UserSession.objects.filter(user=user).delete()
    UserSession.objects.create(
        user=user, session_key=request.session.session_key
    )
