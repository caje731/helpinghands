"""
Django settings for helpinghands project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import helpinghands.config as config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9wxv!i8rtf$te7$ll1gbqk5i@okuw^9slr3a2az2zwe8%1aalo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get_env() == config.ENV_CODES['DEV']

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'caje731.pythonanywhere.com',
    'www.helpinghands.gives'
]

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "webmaster.hhg@gmail.com"
EMAIL_HOST_PASSWORD = os.environ['HH_EMAIL_PASS']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Application definition

INSTALLED_APPS = [
    'admin_view_permission',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', # required by django-photologue
    'donations',
    'nested_admin',
    'photologue',
    'sortedm2m',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MEDIA_ROOT = '/var/www/helpinghands/media/'
MEDIA_URL = '/media/'
ROOT_URLCONF = 'helpinghands.urls'

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

WSGI_APPLICATION = 'helpinghands.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = config.get_db_settings()

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'+\
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'+\
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'+\
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'+\
                '.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'auth.User'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/caje731/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "bower_components"),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
# ======== BOWER ==========
INSTALLED_APPS += ('djangobower',)
STATICFILES_FINDERS += ('djangobower.finders.BowerFinder',)
BOWER_COMPONENTS_ROOT = BASE_DIR

# Bower does not check for missing dependencies, so make sure requirements
# are mentioned in the right order.
# for example Bootstrap requires jQuery, so install jQuery first.
BOWER_INSTALLED_APPS = (
    'jquery#2.1.4',
    'bootstrap#3.3.6',
    'bootstrap-material-design#0.5.6',
    'snap.svg#0.4.1',
    'animate.css#3.2.3',
    'jquery-validation#1.14.0',
    'snackbarjs#1.0.0',
)
