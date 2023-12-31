"""
Django settings for band project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sweetify
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x=4s+t&j0dm*i__e5%m42&asr^esw@#j9815w*1re__v*k_h#$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/redirect'
LOGIN_URL = 'login'
# Application definition

DEFAULT_FROM_EMAIL = "Star Gate Credit Union <stargatecredits@gmail.com>"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'stargatecredits@gmail.com'
EMAIL_HOST_PASSWORD = 'hlktfouivusrnovm'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'sweetify',
    'tz_detect',
    'crispy_forms',
    'landing',
    'g_recaptcha',
    'django.contrib.humanize',
    'rest_framework',
    'corsheaders'

]

GOOGLE_RECAPTCHA_SITE_KEY = "6Le9xicaAAAAAIvK1KKDO836byypX2jZ9NI5E9IB"
GOOGLE_RECAPTCHA_SECRET_KEY = "6Le9xicaAAAAAN-RnjuExHv6UnI6QncuT2TBuN6s"

CORS_ORIGIN_WHITELIST = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:9000",
    "https://account.stargate.online",
    "https://app.stargate.online"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=20),
}

SESSION_EXPIRE_SECONDS = 600  # 600 seconds = 10 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = 'login2'

ROOT_URLCONF = 'band.urls'

AUTH_USER_MODEL = 'app.User'

REST_FRAMEWORK = {
    'UNICODE_JSON': True,
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'error',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    )
}

sweetify.DEFAULT_OPTS = {
    'showConfirmButton': False,
    'timer': 2500,
    'allowOutsideClick': True,
    'confirmButtonText': 'OK',
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

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

WSGI_APPLICATION = 'band.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

SECURE_SSL_REDIRECT = False
# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR+"/assets", ]
# STATIC_ROOT = '/home/cgtbmybu/api.hefeiglobal.com/static'
# MEDIA_ROOT = '/home/cgtbmybu/api.hefeiglobal.com/media'



