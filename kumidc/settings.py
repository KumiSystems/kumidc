from pathlib import Path

import json

from autosecretkey import AutoSecretKey


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = AutoSecretKey(BASE_DIR / "config.ini", template="config.dist.ini")
SECRET_KEY = CONFIG_FILE.secret_key

DEBUG = CONFIG_FILE.config.getboolean("App", "Debug", fallback=False)

ALLOWED_HOSTS = json.loads(CONFIG_FILE.config["App"]["Hosts"])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'oidc_provider',
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

ROOT_URLCONF = 'kumidc.urls'

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

WSGI_APPLICATION = 'kumidc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if "MySQL" in CONFIG_FILE.config:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': CONFIG_FILE.config.get("MySQL", "Database"),
            'USER': CONFIG_FILE.config.get("MySQL", "Username"),
            'PASSWORD': CONFIG_FILE.config.get("MySQL", "Password"),
            'HOST': CONFIG_FILE.config.get("MySQL", "Host", fallback="localhost"),
            'PORT': CONFIG_FILE.config.getint("MySQL", "Port", fallback=3306)
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "core.User"

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
STATIC_ROOT = CONFIG_FILE.config.get("App", "StaticDir", fallback=BASE_DIR / "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# OIDC Configuration

OIDC_USERINFO = 'core.oidc.userinfo'
OIDC_IDTOKEN_INCLUDE_CLAIMS = True