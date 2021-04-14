"""
Django settings for lookaway project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

### Site variables

# When a new member is created, set the limit for number of bytes they
# can use in the media directory. 10**9 = 1 gigabyte.
# If you need space on your media storage for backups,
# then the default should be < total storage capacity / n members / 2
# to prevent the disk from getting too full.
# Example:
# You have a media directory on a filesystem with 500GB available.
# You have 10 members total.
# 500GB / 10 / 2 = 25GB or 10**9*25
# If all 10 members are using 100% of their storage then
# you are using 250GB and have 250GB of space reserved for creating a backup.

DEFAULT_MEMBER_STORAGE = 10**9*2 # 2GB

MEDIA_SETTINGS = {
    'ffmpeg_path': '/usr/bin/ffmpeg',
    'image': {
        'max_height': 2500,
        'max_width': 2500,
        'thumbnail': {
            'max_height': 250,
            'max_width': 250,
        },
    },
    'sound': {
        'bitrate': '1000K',
        'crf': '10', # Lower value means better quality
        'qmin': '0', # "
        'qmax': '50',# "
    },
    'video': {
        'bitrate': '1000K',
        'crf': '10', # Lower value means better quality
        'qmin': '0', # "
        'qmax': '50',# "

    },
}

# Any member that joined before the FOUNDER_CUTOFF date
# will be considered a founder.
                       # year, mo, day
from datetime import datetime
FOUNDER_CUTOFF = datetime(2021, 1, 1)

###############################################################################
### Be careful changing things under this line ###

import os
from django.contrib.messages import constants as messages
from django.urls import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'testserver',
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
    'objects',
    'documentation',
    'posts',
    'music',
    'art',
    'crypto',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lookaway.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'lookaway.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DJANGO_DATABASE_NAME'],
        'USER': os.environ['DJANGO_DATABASE_USER'],
        'PASSWORD': os.environ['DJANGO_DATABASE_PASSWORD'],
        'HOST': os.environ['DJANGO_DATABASE_HOST'],
        'PORT': os.environ['DJANGO_DATABASE_PORT'],
    }
}

# Fix for Changes in Django 3.2
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = "/var/www/html/static/"
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
#LOGOUT_REDIRECT_URL = 'home'
#LOGIN_REDIRECT_URL = 'home'

# Media Files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Bootstrap stuff

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ['ES_FROM']
EMAIL_HOST = os.environ['ES_HOST']
EMAIL_PORT = os.environ['ES_PORT']
EMAIL_HOST_USER = os.environ['ES_USER']
EMAIL_HOST_PASSWORD = os.environ['ES_PASS']
EMAIL_USE_TLS = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.environ['DJANGO_LOG_PATH'],
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
