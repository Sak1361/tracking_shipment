"""
Django settings for tracking_shipment project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x#ukhp9=l=jz%$m@57dt7*2=2nf_i3d8w#t@ff)yu--woz+mkb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracking',
    'bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'global_login_required.GlobalLoginRequiredMiddleware',  # ログインしなくてもいいページ設定
]

ROOT_URLCONF = 'tracking_shipment.urls'

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

WSGI_APPLICATION = 'tracking_shipment.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}"""


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'tracking/static')
LOGIN_URL = 'tracking:login'     # ログイン
LOGOUT_URL = 'tracking:logout'  # ログアウト
# ログイン後トップページにリダイレクト
LOGIN_REDIRECT_URL = 'tracking:search'
# ログアウト後はログインページに
LOGOUT_REDIRECT_URL = 'tracking:top'

# Eメール用
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# メールサーバーへの接続設定
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sa1361ku@gmail.com'
EMAIL_HOST_PASSWORD = 'hlkkzqvuttkfcuyu'
EMAIL_USE_TLS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tracking_django',  # DB name
        'USER': 'root',
        "HOST": "127.0.0.1",
        "PORT": "3306",
        'OPTIONS': {
                # 'read_default_file': '/path/to/my.cnf',
                'init_command': 'SET default_storage_engine=INNODB',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
ALLOWED_HOSTS = []

PUBLIC_PATHS = [  # ログインが必要ないページ
    '/login/',
    '/top/',
    '/user_create/',
    '/user_create/done/',
    '/user_create/complete/<token>',
]
