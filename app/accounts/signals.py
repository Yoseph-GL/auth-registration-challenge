from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import UserSession


@receiver(user_logged_in)
def enforce_single_session(sender, request, user, **kwargs):
    # Borrar la sesión vieja y guardar la nueva para mantener una sola sesión activa
    UserSession.objects.filter(user=user).delete()
    UserSession.objects.create(
        user=user, session_key=request.session.session_key
    )
