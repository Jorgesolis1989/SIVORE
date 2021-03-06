"""
Django settings for SIVORE project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url



import os
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret keybootstrap3 used in production secret!
SECRET_KEY = 'k2t&n^74q8+($t(!__8+vc)$@(ya3lt##g1oy=a7ka29=wv$8s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = {
    'bootstrap3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'corporaciones',
    'votantes',
    'candidatos',
    'planchas',
    'jornadas',
    'votaciones',
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

)

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend', "usuarios.backends.BackendUsuarios")

ROOT_URLCONF = 'SIVORE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates' ,
        'DIRS': [os.path.join(BASE_DIR,'templates'),
                 os.path.join(BASE_DIR,'usuarios/templates'),
                 os.path.join(BASE_DIR,'corporaciones/templates'),
                 os.path.join(BASE_DIR,'candidatos/templates'),
                 os.path.join(BASE_DIR,'votantes/templates'),
                 os.path.join(BASE_DIR,'planchas/templates'),
                 os.path.join(BASE_DIR,'jornadas/templates'),
                 os.path.join(BASE_DIR,'votaciones/templates'),],


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


#TEMPLATE_DIRS = (
#    '/home/SIVORE/usuarios/templates',
#)


WSGI_APPLICATION = 'SIVORE.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'sivore',
    'USER': 'sivore',
    'PASSWORD': 'sivorepass',
    'HOST': '127.0.0.1',
    'PORT': '5432',
    'CONN_MAX_AGE': 500,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'


STATICFILES_DIRS = (
   os.path.join(BASE_DIR, "static"),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('login')

#Email configurations
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sivoreunivalle@gmail.com'
EMAIL_HOST_PASSWORD = 'sivore123@'


MEDIA_ROOT = 'SIVORE/media/'
MEDIA_URL = 'http://localhost:8000/SIVORE/media/'

DATE_INPUT_FORMATS=[
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',
]

TIME_INPUT_FORMATS= [
    '%H:%M:%S',
    '%H:%M',
    '%I:%M %p',
]