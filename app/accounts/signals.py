from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver

from .models import UserSession


@receiver(user_logged_in)
def enforce_single_session(sender, request, user, **kwargs):
    """US02 AC12: kill the previous session (if any), then track the new one."""
    UserSession.objects.filter(user=user).delete()
    Session.objects.filter(session_key=request.session.session_key).delete()

    request.session.cycle_key()
    UserSession.objects.create(
        user=user, session_key=request.session.session_key
    )
