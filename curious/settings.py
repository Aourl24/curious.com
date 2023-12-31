"""
Django settings for fatwa project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
#from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['192.168.43.1']

#SECRET_KEY=config('my_key')
SECRET_KEY = 'django-insecure-!ty9w7k)$02e48otuxekbx8j2805o-5wni(%ety5lycf$&qa-m'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'allauth', 
    'allauth.account', 
    'allauth.socialaccount', 
    'forum', 
    'ask',
    'crispy_forms', 
    'hitcount', 
    'notifications',
    'freezy'
]

#DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}

CRISPY_TEMPLATE_PACK= 'bootstrap4'

SITE_ID=1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'curious.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'), )],
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

WSGI_APPLICATION = 'curious.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'Awwal', 
#        'USER': 'curious', 
#        'PASSWORD': 'Aourl2001',
#        'HOST': '127.0.0.1', 
#        'PORT': '8000',
#    }
#}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS=(str(BASE_DIR.joinpath('static')), )

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL='/media/'
MEDIA_ROOT= str(BASE_DIR.joinpath('media'))
LOGIN_REDIRECT_URL='/page/home'
#LOGOUT_REDIRECt_URL='//'

AUTHENTICATION_BACKENDS = [ 'django.contrib.auth.backends.ModelBackend',
'allauth.account.auth_backends.AuthenticationBackend'] 
# EMAIL_BACKEND so allauth can proceed to send confirmation emails
# ONLY for development/testing use console 
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

# Custom allauth settings
# Use email as the primary identifier
#ACCOUNT_AUTHENTICATION_METHOD = 'email'
#ACCOUNT_EMAIL_REQUIRED = True

# Make email verification mandatory to avoid junk email accounts
#ACCOUNT_EMAIL_VERIFICATION = 'mandatory' 

# Eliminate need to provide username, as it's a very old practice
#ACCOUNT_USERNAME_REQUIRED = True