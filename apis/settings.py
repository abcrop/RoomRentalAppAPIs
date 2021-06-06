"""
Django settings for apis project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from ntpath import join
import os
import dotenv
import django_heroku
import rest_framework
import whitenoise
import dj_database_url
from pathlib import Path
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.conf.global_settings import DATETIME_FORMAT

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Initializing dotenv
try:
    dotenv_file = dotenv.find_dotenv(filename='.env')

    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)
        
        #apply local_properties in LOCALHOST
        try:
            from endpoints.settings.local_properties import *
        except: 
            print("No Such File Found in Localhost")
                
    else: 
        #apply heroku_properties in HEROKU PRODUCTION
        try:
            from endpoints.settings.heroku_properties import *
        except: 
            print("No Such File Found in Heroku Production")
except Exception as e:
    print(e)

SECRET_KEY = os.environ.get('SECRET_KEY')

# Application definition
AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'endpoints',
    'rest_framework',
    'oauth2_provider',
    'debug_toolbar',
    'django_filters',
    'coreapi',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #Checks wheather request contains token 
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'apis.urls'

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

WSGI_APPLICATION = 'apis.wsgi.application'
     
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

#for encrypting and decrypting hash passwords
PASSWORD_HASHERS = [
    # 'endpoints.hashers.CustomPBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

USE_I18N = True

USE_L10N = True

USE_TZ = True


#oauth config
LOGIN_URL='/admin'+ os.environ.get('ADMIN') + '/login/'

#static files (CSS, JS, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

#in heroku, to find static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

#django doesn't support static files in production so whitenoise comes into play
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'endpoints.AppUser'

OAUTH2_PROVIDER = {
    #Token expires at $seconds
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60*60*5,
    # 'OAUTH_DELETE_EXPIRED': True,
    # 'SCOPES': {
    #     'read': 'Read scope', 
    #     'write': 'Write scope',
    #     'groups': 'Access to your groups',
    # }
}

REST_FRAMEWORK = {  
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],  
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    'DEFAULT_PAGINATION_CLASS': 'endpoints.paginations.SmallResultsSetPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/day',
        'user': '1000/day'
    },
    
    'DEFAULT_RENDERER_CLASSES': (
        #Disables browsable api feature for production
        'rest_framework.renderers.JSONRenderer',
    ) if not DEBUG 
    else (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
    
    #439 error while user has exceeded throtle rate

}


#adding this to avoid warning about AutoFiled
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

#Django debug_toolbar
INTERNAL_IPS = {
    '127.0.0.1',
}

# For debug_toolbar logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'incremental': True,
    'root': {
        'level': 'DEBUG',
    },
}

django_heroku.settings(locals())