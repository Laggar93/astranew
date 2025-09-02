import os
from pathlib import Path
from astra import config


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config.secret_key


DEBUG = config.debug


ALLOWED_HOSTS = config.hosts


INSTALLED_APPS = [
    'products.templatetags.float',
    'products.templatetags.length',
    'products.templatetags.inside',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'adminsortable2',
    'django_unused_media',
    'products.apps.ProductsConfig',
    'manufacturers.apps.ManufacturersConfig',
    'about.apps.AboutConfig',
    'contacts.apps.ContactsConfig',
    'main.apps.MainConfig',
    'import_export',
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


ROOT_URLCONF = 'astra.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'astra.context_processor.globals',
            ],
        },
    },
]


if config.wsgi:
    WSGI_APPLICATION = 'astra.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'astra/static/')
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'allowedContent': True,
        'toolbar_Custom': [
            ['Format'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Source'],
            ['Bold'],
        ]
    },
}


#SESSION_COOKIE_SECURE = True
#SECURE_HSTS_SECONDS = 1
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_SSL_REDIRECT = config.secure_ssl_redirect
#CSRF_COOKIE_SECURE = True
#SECURE_HSTS_PRELOAD = True