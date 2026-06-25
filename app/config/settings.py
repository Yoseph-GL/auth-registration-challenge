import os
from pathlib import Path

# Construir la ruta base del proyecto para no hardcodear directorios
BASE_DIR = Path(__file__).resolve().parent.parent

# Fail-fast: forzar crash si no existe la variable en el entorno
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.environ.get('DEBUG', '') == 'True'

# Hosts permitidos desde variable de entorno; defaults para desarrollo local
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0'
).split(',')

# Dejar el admin de Django activo para comandos como createsuperuser
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'accounts.middleware.SingleSessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Apuntar al directorio raíz de templates para compartir layouts
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Conectar al servicio Docker; los defaults permiten correr sin Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'auth_challenge'),
        'USER': os.environ.get('DB_USER', 'django'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'django_secret'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Tres validadores estándar de Django más el mío que exige letra y número
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'accounts.validators.PasswordStrengthValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'

# Agregar el directorio static para los archivos CSS e imágenes
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Decirle a Django que use mi modelo User personalizado con email
AUTH_USER_MODEL = 'accounts.User'

# Definir URLs por nombre para no hardcodear rutas en los templates
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Configurar la sesión para que expire a los 15 minutos de inactividad
SESSION_COOKIE_AGE = 15 * 60  # 15 minutos de inactividad
SESSION_SAVE_EVERY_REQUEST = True
