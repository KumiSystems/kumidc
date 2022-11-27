from django.urls import reverse_lazy

from pathlib import Path
from urllib.parse import urljoin

import json

import saml2

from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED
from saml2.sigver import get_xmlsec_binary

from autosecretkey import AutoSecretKey


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = AutoSecretKey(BASE_DIR / "config.ini", template="config.dist.ini")
SECRET_KEY = CONFIG_FILE.secret_key

DEBUG = CONFIG_FILE.config.getboolean("App", "Debug", fallback=False)

ALLOWED_HOSTS = json.loads(CONFIG_FILE.config["App"]["Hosts"])
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]
BASE_URL = CONFIG_FILE.config["App"]["BaseURL"]

CERTIFICATE_DIR = Path(CONFIG_FILE.config.get("App", "CertificateDir", fallback=BASE_DIR / "certificates"))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'phonenumber_field',
    'crispy_forms',
    'ajax_datatable',

    'core',
    'authentication',
    'frontend',

    'oidc_provider',
    'djangosaml2idp',
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

LOGIN_URL = reverse_lazy("auth:login")
LOGIN_REDIRECT_URL = reverse_lazy("frontend:dashboard")

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
OIDC_AFTER_USERLOGIN_HOOK = "authentication.hooks.oidc.authorize_hook"
OIDC_TEMPLATES = {
    'authorize': 'frontend/oidc/authorize.html'
}

# SAML Configuration

SAML_IDP_CONFIG = {
    'debug' : DEBUG,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin']),
    'entityid': urljoin(BASE_URL, '/saml/metadata/'),
    'description': 'KumiDC',

    'service': {
        'idp': {
            'name': 'KumiDC',
            'endpoints': {
                'single_sign_on_service': [
                    (urljoin(BASE_URL, '/saml/sso/post/'), saml2.BINDING_HTTP_POST),
                    (urljoin(BASE_URL, '/saml/sso/redirect/'), saml2.BINDING_HTTP_REDIRECT),
                ],
                "single_logout_service": [
                    (urljoin(BASE_URL, "/saml/slo/post/"), saml2.BINDING_HTTP_POST),
                    (urljoin(BASE_URL, "/saml/slo/redirect/"), saml2.BINDING_HTTP_REDIRECT)
                ],
            },
            'name_id_format': [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
            'sign_response': False,
            'sign_assertion': False,
            'want_authn_requests_signed': False,
        },
    },

    # Signing
    'key_file': str(CERTIFICATE_DIR / 'saml.key'),
    'cert_file': str(CERTIFICATE_DIR / 'saml.crt'),

    # Encryption
    'encryption_keypairs': [{
        'key_file': str(CERTIFICATE_DIR / 'saml.key'),
        'cert_file': str(CERTIFICATE_DIR / 'saml.crt'),
    }],

    'valid_for': 365 * 24,
}

SAML_IDP_SP_FIELD_DEFAULT_PROCESSOR = 'core.saml.processors.SAMLProcessor'
SAML_IDP_MULTIFACTOR_VIEW = "frontend.views.saml.SAMLMultiFactorView"

SAML_AUTHN_SIGN_ALG = saml2.xmldsig.SIG_RSA_SHA256
SAML_AUTHN_DIGEST_ALG = saml2.xmldsig.DIGEST_SHA256

SAML_IDP_SHOW_CONSENT_FORM = True
SAML_IDP_SHOW_USER_AGREEMENT_SCREEN = True

DEFAULT_SPCONFIG = {
    'processor': 'uniauth_saml2_idp.processors.ldap.LdapUnicalMultiAcademiaProcessor',
    'attribute_mapping': {
        "cn": "cn",
        "eduPersonEntitlement": "eduPersonEntitlement",
        "eduPersonPrincipalName": "eduPersonPrincipalName",
        "schacHomeOrganization": "schacHomeOrganization",
        "eduPersonHomeOrganization": "eduPersonHomeOrganization",
        "eduPersonAffiliation": "eduPersonAffiliation",
        "eduPersonScopedAffiliation": "eduPersonScopedAffiliation",
        "eduPersonTargetedID": "eduPersonTargetedID",
        "mail": ["mail", "email"],
        "email": ["mail", "email"],
        "schacPersonalUniqueCode": "schacPersonalUniqueCode",
        "schacPersonalUniqueID": "schacPersonalUniqueID",
        "sn": "sn",
        "givenName": ["givenName", "another_possible_occourrence"],
        "displayName": "displayName",
    },
    'display_name': 'Unical SP',
    'display_description': 'This is for test purpose',
    'display_agreement_message': 'Some information about you has been requested',
    'signing_algorithm': saml2.xmldsig.SIG_RSA_SHA256,
    'digest_algorithm': saml2.xmldsig.DIGEST_SHA256,
    'disable_encrypted_assertions': True,
    'show_user_agreement_screen': SAML_IDP_SHOW_USER_AGREEMENT_SCREEN
}

# Session Timeouts

REVERIFY_AFTER_INACTIVITY_MINUTES = 5