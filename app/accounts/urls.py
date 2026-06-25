from django.urls import path

from .views import DeactivateView, HomeView, LoginView, RegisterView

# Registrar las rutas: registro, login, home y desactivación de cuenta
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("", HomeView.as_view(), name="home"),
    path("deactivate/", DeactivateView.as_view(), name="deactivate"),
]
