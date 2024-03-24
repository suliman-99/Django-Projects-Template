"""
Django settings for Project_Name project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from decouple import config
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from logger.configuration import LOGGING_DICT
import firebase_admin

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])

INTERNAL_IPS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'users',
    'django_seeding',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'corsheaders',
    'dbbackup',
    'fcm_django',
    'drf_spectacular',

    'logger',
    'content_type',
    'notification',
    'seeder',
    'test_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # locale
    'corsheaders.middleware.CorsMiddleware', # cors
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middlewares.ResponseCoordinatorMiddleware', # ResponseCoordinator
]

ROOT_URLCONF = 'Project_Name.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'Project_Name.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'NAME': config('DATABASE_NAME'),
    }
}

ACTIVATE_REDIS_CACHE = config('ACTIVATE_REDIS_CACHE', cast=bool, default=True)
if ACTIVATE_REDIS_CACHE:
    REDIS_KEY_PREFIX = config('REDIS_KEY_PREFIX', default='project_name_cache_')
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": REDIS_KEY_PREFIX,
        },
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'common.exception_handler.custom_exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomPageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT'),
    'REFRESH_TOKEN_LIFETIME': timedelta(config('REFRESH_TOKEN_LIFETIME', cast=int, default=30)),
    'ACCESS_TOKEN_LIFETIME': timedelta(config('ACCESS_TOKEN_LIFETIME', cast=int, default=1)),
    "UPDATE_LAST_LOGIN": True,
}

AUTHENTICATION_BACKENDS = [
    'users.backends.AdminEmailBackend',
    'users.backends.AdminPhoneNumberBackend',
]

EMAIL_VERIFICATION_CODE_ALWAYS_123456 = config('EMAIL_VERIFICATION_CODE_ALWAYS_123456', cast=bool, default=False)

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

ACTIVATE_FIREBASE = config('ACTIVATE_FIREBASE', cast=bool, default=False)
if ACTIVATE_FIREBASE:
    GOOGLE_APPLICATION_CREDENTIALS = config('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_APPLICATION_CREDENTIALS_OBJECT = firebase_admin.credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
    GOOGLE_APPLICATION = firebase_admin.initialize_app(GOOGLE_APPLICATION_CREDENTIALS_OBJECT)

ACTIVATE_TWILIO = config('ACTIVATE_TWILIO', cast=bool, default=True)
if ACTIVATE_TWILIO:
    TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
    TWILIO_SERVICE = config('TWILIO_SERVICE')
    
LOGGING = LOGGING_DICT
ADMINS = config('ADMINS', cast=lambda v: tuple(tuple(o.strip() for o in s.split(',')) for s in v.split('|')))

SEEDING_ON_RUNSERVER = config('SEEDING_ON_RUNSERVER', cast=bool, default=True)

# Configure backup storage location (optional)
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'backup/backups/'}
BACKUP_FILE_PREFIX = config('BACKUP_FILE_PREFIX', cast=str, default='project_name')

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    AUTH_PASSWORD_VALIDATORS = []

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project_Name API',
    'DESCRIPTION': 'Project_Name description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}
