# Exponer la aplicación como callable WSGI para el servidor web
import os

from django.core.wsgi import get_wsgi_application

# setdefault respeta la variable si ya viene del servidor (gunicorn, etc.)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
