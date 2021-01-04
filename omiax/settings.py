"""
Django settings for omiax project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta
from django.conf.locale.en import formats as en_formats
from environ import Env

env = Env()

Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = [x for x in env.list('ALLOWED_HOSTS')]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_rest_passwordreset',
    'tinymce',
    'django_q',
    # my apps
    "user",
    "lodge",
    "payments",
]


en_formats.DATETIME_FORMAT = "d-m-Y H:i:s"

# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html
# https://mattsegal.dev/simple-scheduled-tasks.html
Q_CLUSTER = {
    "name": "omiax",
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    "orm": "default",  # Use Django's ORM + database for broker
}

# @TODO cron jobs
# send reminder emails or text message for room expiry date
# flushexpiredtokens

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':
    ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('rest_framework_simplejwt.authentication.JWTAuthentication', )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1440),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT', ),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', ),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'csp.middleware.CSPMiddleware',
]

# CORS_ORIGIN_ALLOW_ALL = False

# CORS_ORIGIN_WHITELIST = ['http://' + x for x in env.list('ALLOWED_HOSTS')]
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000', 'http://localhost:3000']


ROOT_URLCONF = "omiax.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['omiax/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "omiax.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }
# if DEBUG is False:
DATABASES = {
    "default": env.db()
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-NG"

# @TODO change later
# TIME_ZONE = "UTC"
TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

AUTH_USER_MODEL = "user.User"

# Content Security Policy
# set iframe path
# CSP_DEFAULT_SRC = ["'none'", ]

# CSP_FRAME_SRC = ["http://127.0.0.1:8000", "http://127.0.0.1:3000"]
# CSP_FRAME_ANCESTORS = ["'self'", "http://127.0.0.1:3000"]

# X_FRAME_OPTIONS = 'ALLOW-FROM http://127.0.0.1:3000'

# TINYMCE_DEFAULT_CONFIG = {
#     'cleanup_on_startup': True,
#     'custom_undo_redo_levels': 20,
#     'selector': 'textarea',
#     'theme': 'silver',
#     'plugins': '''
#             textcolor save link image media preview codesample contextmenu
#             table code lists fullscreen  insertdatetime  nonbreaking
#             contextmenu directionality searchreplace wordcount visualblocks
#             visualchars code fullscreen autolink lists  charmap print  hr
#             anchor pagebreak
#             ''',
#     'toolbar1': '''
#             fullscreen preview bold italic underline | fontselect,
#             fontsizeselect  | forecolor backcolor | alignleft alignright |
#             aligncenter alignjustify | indent outdent | bullist numlist table |
#             | link image media | codesample |
#             ''',
#     'toolbar2': '''
#             visualblocks visualchars |
#             charmap hr pagebreak nonbreaking anchor |  code |
#             ''',
#     'contextmenu': 'formats | link image',
#     'menubar': True,
#     'statusbar': True,
# }
