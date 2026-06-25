from django.urls import path

from .views import DeactivateView, HomeView, LoginView, RegisterView

# Cada name= se usa en templates ({% url %}) y en settings (LOGIN_URL, etc.)
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("", HomeView.as_view(), name="home"),
    path("deactivate/", DeactivateView.as_view(), name="deactivate"),
]
