from django.contrib import admin
# Usar el LogoutView genérico de Django para no reinventar el cierre de sesión
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Montar accounts en la raíz para que /login y /register respondan directo
    path('', include('accounts.urls')),
    # logout va en la raíz porque es una acción global, no exclusiva de accounts
    path('logout/', LogoutView.as_view(), name='logout'),
]
