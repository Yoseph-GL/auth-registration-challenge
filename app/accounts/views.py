from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, RegisterForm
from .models import LoginAttempt, User


class RegisterView(CreateView):
    # Mostrar mensaje de éxito y redirigir al login cuando el registro es válido

    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful! Please log in.")
        return response


class LoginView(BaseLoginView):
    # Verificar bloqueo y desactivación antes de autenticar

    form_class = LoginForm
    template_name = "accounts/login.html"

    _LOCKOUT_HOURS = 2
    _LOCKOUT_MAX_FAILURES = 3
    _LOCKOUT_MESSAGE = (
        "Your account has been blocked for 2 hours due to "
        "multiple failed login attempts."
    )
    _DEACTIVATED_MESSAGE = (
        "This account has been deactivated. Please contact support."
    )

    def _get_user_or_none(self, email):
        # Buscar el usuario por email; retornar None si no existe
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def _is_locked_out(self, user):
        # Verificar si el usuario superó el límite de fallos en la ventana de tiempo
        cutoff = timezone.now() - timedelta(hours=self._LOCKOUT_HOURS)
        failures = LoginAttempt.objects.filter(
            user=user, success=False, timestamp__gte=cutoff
        )
        return failures.count() >= self._LOCKOUT_MAX_FAILURES

    def _render_clean_form(self, request):
        return render(
            request, self.template_name, {"form": self.get_form_class()()}
        )

    def form_valid(self, form):
        user = form.get_user()
        # Limpiar historial de fallos tras un login exitoso para evitar bloqueos falsos
        LoginAttempt.objects.filter(user=user).delete()
        messages.success(self.request, "Login successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        email = self.request.POST.get("username", "")
        user = self._get_user_or_none(email)
        if user is None:
            return super().form_invalid(form)

        # Registrar este fallo antes de contar el total para aplicar el lockout
        LoginAttempt.objects.create(user=user, success=False)

        if self._is_locked_out(user):
            messages.error(self.request, self._LOCKOUT_MESSAGE)
            return self._render_clean_form(self.request)
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        # Bloquear el request desde el inicio si la cuenta está desactivada o en lockout
        email = request.POST.get("username", "")
        if email:
            user = self._get_user_or_none(email)
            if user is not None:
                if not user.is_active:
                    messages.error(request, self._DEACTIVATED_MESSAGE)
                    return self._render_clean_form(request)

                if self._is_locked_out(user):
                    messages.error(request, self._LOCKOUT_MESSAGE)
                    return self._render_clean_form(request)

        return super().dispatch(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    # Mostrar página principal con bienvenida y opciones de cuenta después del login

    template_name = "accounts/home.html"


class DeactivateView(View):
    # Desactivar la cuenta sin borrar los datos del usuario

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            user.is_active = False
            user.save(update_fields=["is_active"])
            messages.success(request, "Your account has been deactivated.")
        return redirect("login")
