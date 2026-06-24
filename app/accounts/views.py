from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, RegisterForm
from .models import LoginAttempt, User


class RegisterView(CreateView):
    """US01: Registration with success message and redirect to login."""

    model = User
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful! Please log in.")
        return response


class LoginView(BaseLoginView):
    """US02: Login with lockout (3 fails / 2h), deactivation check (US03)."""

    form_class = LoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        """Wipe failed-attempt history on successful login."""
        user = form.get_user()
        LoginAttempt.objects.filter(user=user).delete()
        messages.success(
            self.request,
            f"Welcome {user.full_name}! To logout click here",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Log the failed attempt. If >= 3 in the last 2 hours, show lockout."""
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
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        """Pre-form checks: deactivated account or existing lockout → block."""
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
                        request, self.template_name, {"form": self.get_form()}
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
                        request, self.template_name, {"form": self.get_form()}
                    )

        return super().dispatch(request, *args, **kwargs)


class HomeView(TemplateView):
    """Post-login landing page with welcome message and logout link."""

    template_name = "accounts/home.html"


class DeactivateView(TemplateView):
    """US03: Soft-delete — sets is_active=False, keeps data in the DB."""

    template_name = "accounts/deactivate_confirm.html"

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            user.is_active = False
            user.save(update_fields=["is_active"])
            messages.success(request, "Your account has been deactivated.")
        return redirect("login")
