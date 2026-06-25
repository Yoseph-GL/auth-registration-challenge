from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver

from .models import UserSession


@receiver(user_logged_in)
def enforce_single_session(sender, request, user, **kwargs):
    """US02 AC12: kill the previous session (if any), then track the new one.

    Django's auth_login() already calls session.cycle_key() before firing
    this signal, so request.session.session_key is already the new key.
    We grab the old UserSession to delete the old django_session row,
    then track the current (new) session key.
    """
    old = UserSession.objects.filter(user=user).first()
    if old:
        Session.objects.filter(session_key=old.session_key).delete()
    UserSession.objects.filter(user=user).delete()

    UserSession.objects.create(
        user=user, session_key=request.session.session_key
    )
