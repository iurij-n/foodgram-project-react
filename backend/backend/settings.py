"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'apv$)3@w4i+ge(tc*crga0#po4j!-xf94*lfm2*)f3dl*pklzm'
SECRET_KEY = os.getenv('SECRET_KEY', default='okdd2!0ks1k5q!*@29q3tnlftr_g4zo@8+t%x*2+=a^j!6')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

EMPTY_VALUE_DISPLAY = '-пусто-'

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# ADD_RECIPE_ERROR_MESSAGES = {
#     'Favorites': {
#         'POST': f'Рецепт \"{recipe.name}\" '
#                 'уже есть в избранном у пользователя '
#                 f'{user.username}',
#         'DELETE': f'У пользователя {user.username} '
#                   f'в избранном нет рецепта \"{recipe.name}\"'},
#     'ShoppingCart': {
#         'POST': f'Рецепт \"{recipe.name}\" '
#                 'уже есть в списке покупок у пользователя '
#                 f'{user.username}',
#         'DELETE': f'У пользователя {user.username} '
#                   f'в списке покупок нет рецепта \"{recipe.name}\"'}
# }


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recipe.apps.RecipeConfig',
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
]

AUTH_USER_MODEL = 'users.User'

DJOSER = {
    'LOGIN_FIELD': 'email',
    # 'REQUIRED_FIELDS': ['username', 'first_name', 'last_name', 'password'],
    # 'HIDE_USERS': False,
    'SERIALIZERS': {
        # 'user_create': 'api.serializers.CustomUserCreateSerializer',
        # 'user': 'api.serializers.UserDetailSerializer',
        # 'user': 'api.serializers.CustomUserCreateSerializer',
        'current_user': 'api.serializers.CustomUserSerializer',
    },
    # 'PERMISSIONS': {
    #     'user_list': ['rest_framework.permissions.AllowAny',],
    # }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', 
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
#         'NAME': os.getenv('DB_NAME', default='postgres'),
#         'USER': os.getenv('POSTGRES_USER', default='postgres'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='ks1k5q!*@29q3tnl'),
#         'HOST': os.getenv('DB_HOST', default='localhost'),
#         # 'PORT': os.getenv('DB_PORT', default='5432')
#         'PORT': os.getenv('DB_PORT', default='')
#     }
# }


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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
