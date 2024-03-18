"""
Django settings for rtback project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

IS_DEVELOPMENT = os.getenv('IS_DEVELOPMENT') == 'TRUE'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#  Media base dir
MEDIA_ROOT = os.path.join(os.getenv('MEDIA_DIR'), 'media')

# Image base dir
MEDIA_URL = '/media/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l&dw^_-lz1o*+akmdgo4k09=6ko010+q(dqfi+c_m3c$hqe%3#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if IS_DEVELOPMENT else False

ALLOWED_HOSTS = ['192.168.2.79','192.168.2.16', 'localhost', '127.0.0.1', '192.168.2.144', '35.209.176.71', ' 70.31.50.163', '34.130.51.136']


# Application definition

INSTALLED_APPS = [
    'inventory.apps.InventoryConfig',
    'staff.apps.StaffConfig',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     'http://127.0.0.1:8001',
#     'http://localhost:3001',
#     'http://192.168.2.144:3001',
# ]

ROOT_URLCONF = 'rtback.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rtback.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": "ruito",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "34.29.14.234",
        # "HOST": "localhost",
        "PORT": "3306",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# # Log configuration
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         # "console": {
#         #     "class": "logging.StreamHandler",
#         # },
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": "/home/ky/code/RTBack/logs/django.log",
#         },
#     },
#     # "root": {
#     #     "handlers": ["console"],
#     #     "level": "WARNING",
#     # },
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
#             "propagate": False,
#         },
#     },
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            "filename": "django.log",
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
