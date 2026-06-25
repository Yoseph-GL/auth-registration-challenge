from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Montar accounts en la raíz para que /login y /register respondan directo
    path('', include('accounts.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]
