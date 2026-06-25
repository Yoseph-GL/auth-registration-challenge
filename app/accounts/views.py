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
    # Muestro un mensaje de éxito y redirijo al login cuando el registro es válido

    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful! Please log in.")
        return response


class LoginView(BaseLoginView):
    # Verifico si la cuenta está bloqueada o desactivada antes de permitir el login

    form_class = LoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        user = form.get_user()
        LoginAttempt.objects.filter(user=user).delete()
        messages.success(self.request, "Login successful.")
        return super().form_valid(form)

    def form_invalid(self, form):
        email = self.request.POST.get("username", "")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_invalid(form)

        LoginAttempt.objects.create(user=user, success=False)

        cutoff = timezone.now() - timedelta(hours=2)
        failures = LoginAttempt.objects.filter(
            user=user, success=False, timestamp__gte=cutoff
        )
        if failures.count() >= 3:
            messages.error(
                self.request,
                "Your account has been blocked for 2 hours due to "
                "multiple failed login attempts.",
            )
            # Renderizo un formulario limpio para que el mensaje de bloqueo se lea sin distracción
            return render(
                self.request, self.template_name, {"form": self.get_form_class()()}
            )
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        email = request.POST.get("username", "")
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                if not user.is_active:
                    messages.error(
                        request,
                        "This account has been deactivated. "
                        "Please contact support.",
                    )
                    return render(
                        request, self.template_name, {"form": self.get_form_class()()}
                    )

                cutoff = timezone.now() - timedelta(hours=2)
                failures = LoginAttempt.objects.filter(
                    user=user, success=False, timestamp__gte=cutoff
                )
                if failures.count() >= 3:
                    messages.error(
                        request,
                        "Your account has been blocked for 2 hours due to "
                        "multiple failed login attempts.",
                    )
                    return render(
                        request, self.template_name, {"form": self.get_form_class()()}
                    )

        return super().dispatch(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    # Página principal después de login con mensaje de bienvenida y opciones de cuenta

    template_name = "accounts/home.html"


class DeactivateView(View):
    # Desactivo la cuenta del usuario sin borrar sus datos de la base de datos

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            user.is_active = False
            user.save(update_fields=["is_active"])
            messages.success(request, "Your account has been deactivated.")
        return redirect("login")
