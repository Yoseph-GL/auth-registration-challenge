from django.contrib.auth import logout

from .models import UserSession


class SingleSessionMiddleware:
    # Valida que la sesión activa del usuario coincida con la almacenada en DB;
    # si otro login mató esta sesión, fuerza el logout automáticamente.

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                active = UserSession.objects.get(user=request.user)
            except UserSession.DoesNotExist:
                # Sin registro de sesión — recrearlo para que el usuario no quede
                # bloqueado si el signal de login falló
                UserSession.objects.create(
                    user=request.user,
                    session_key=request.session.session_key,
                )
            else:
                if active.session_key != request.session.session_key:
                    logout(request)

        return self.get_response(request)
