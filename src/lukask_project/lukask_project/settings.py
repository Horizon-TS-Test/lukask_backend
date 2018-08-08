"""
Django settings for lukask_project project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8$y=e+2*@5!zz3*67u(t9iub+1ug&&3t!7o12#0=j!1r-^akq)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['172.31.0.103', '54.233.211.204','ec2-54-233-211-204.sa-east-1.compute.amazonaws.com', 'back.lukaksarticles.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lukask_app',
    'rest_framework',
    'rest_framework.authtoken',
	'sslserver',
    #'corsheaders',
    'channels',
    'channels_api',
    'django_filters'
    #'tornado_websockets',
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

ROOT_URLCONF = 'lukask_project.urls'

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

WSGI_APPLICATION = 'lukask_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lukask_db',
        'USER': 'lukask_back_user',
        'PASSWORD': 'lukask',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 0
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/repositorio_lukask/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'repositorio_lukask')

#MEDIA_URL = '/repositorio_lukask/'
#MEDIA_ROOT = '/vagrant/src/lukask_project/repositorio_lukask/'

#STATICFILES_DIRS = [
 #   os.path.join(BASE_DIR, "repositorio_lukask"),
#]

AUTH_USER_MODEL = 'lukask_app.UserProfile'


# -----------------------------CORS------------------------
# EVERYBODY WILL BE ABLE TO ACCESS WITH CORS:
# NEXT LINE IS SET WITH FALSE BY DEFAULT
# CORS_ORIGIN_ALLOW_ALL = True

# I JUST WANT TO ALLOW NEXT CLIENT TO ACCESS MY API WITH CORS:
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8000',
)

CSRF_TRUSTED_ORIGINS = (
    '127.0.0.1:8000',
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'PATCH',
    'POST',
    'PUT',
)
# ------------------------------------------------------------------------------

# -------------------------CHANNELS CONFIG:------------------------------
CHANNEL_LAYERS = {
    "default": {
        # "BACKEND": "asgiref.inmemory.ChannelLayer", # USING DAPHNE CHANNEL LAYER FOR DEVELOPMENT
        "BACKEND": "asgi_redis.RedisChannelLayer",  # USING REDIS CHANNEL LAYER FOR PRODUCTION
        "ROUTING": "lukask_project.routing.channel_routing",
        "CONFIG": {
            # USING DOMAIN NAME IN PRODUCTION:
            # "hosts": [("redis-channel-1", 6379), ("redis-channel-2", 6379)]
            # USING LOCALHOST IN DEVELOPMENT:
            "hosts": [("localhost", 6379)]
        }
    },
}

# CHANNELS API CONFIG:
CHANNELS_API = {
    'DEFAULT_PAGE_SIZE': 25
}
# ------------------------------------------------------------------------------

# ---------------------------TORNADO WEBSOCKETS---------------------------------
TORNADO = {
    'port': 9432,
    'handlers': [],
    'settings': {
        'debug': True,
    },
}


#--------------------------------------------------------------------------------
#                   PAGINATION
#--------------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}
