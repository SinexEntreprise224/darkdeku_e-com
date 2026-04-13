import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- SÉCURITÉ ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-this')

# DEBUG est True par défaut en local, mais doit être False sur Railway
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Autorise localhost pour le dev et ton futur domaine Railway
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# --- APPLI ---
INSTALLED_APPS = [
    # WhiteNoise doit être au-dessus de staticfiles si possible
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tes Apps
    'store',

    # Librairies tierces
    'crispy_forms',
    'crispy_bootstrap5',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoiseMiddleware doit être juste après SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'E_com.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'E_com.wsgi.application'

# --- BASE DE DONNÉES ---
# Railway fournit une DATABASE_URL. Si elle n'existe pas, on utilise tes variables individuelles.

# Backup pour le développement classique si aucune URL n'est fournie
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecom_db',      # Le nom créé à l'étape 1
        'USER': 'DarkDeku',    # L'utilisateur créé
        'PASSWORD': 'DarkDeku@',
        'HOST': 'localhost',      # Ou '127.0.0.1'
        'PORT': '5432',           # Port par défaut de Postgres
    }
}
# --- VALIDATION MOT DE PASSE ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALISATION ---
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Compression et mise en cache des fichiers statiques par WhiteNoise
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- CONFIGURATIONS SPÉCIFIQUES ---
AUTH_USER_MODEL = 'store.User'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Sécurité supplémentaire en production
