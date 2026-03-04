"""
Django settings for Bobbin_pro project.
"""

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SECURITY SETTINGS
# =========================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-change-this-in-production"
)

# DEBUG = os.environ.get("DEBUG", "True") == "True"
DEBUG = False

ALLOWED_HOSTS = [
    "bobbin.onrender.com",
    "127.0.0.1",
    "localhost"
]
# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom app
    'Bobbin_app',

    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
]

# =========================
# MIDDLEWARE (IMPORTANT ORDER ⭐)
# =========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise must be after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Bobbin_pro.urls'

# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'Bobbin_app.context_processors.cart_item_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'Bobbin_pro.wsgi.application'

# =========================
# DATABASE (Render Compatible)
# =========================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = []

# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES (PRODUCTION ⭐)
# =========================

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# =========================
# MEDIA FILES
# =========================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =========================
# CRISPY FORMS
# =========================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"