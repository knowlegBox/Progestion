
from pathlib import Path

# import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# env = environ.Env()

# environ.Env.read_env(env_file=str(BASE_DIR / "zimpot" / ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env.bool("DEBUG", default=False)

# ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

SECRET_KEY = 'django-insecure-h%%ua#f31^irky=u_7q6bis6)4+sed7id0g1x#$h0co$wwg3i1'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_htmx",
    'tailwind',
    "theme",
    # 'django_browser_reload',
    'django.contrib.humanize',
    # "debug_toolbar",
    # -----------------
    'account',
    "customers",
    "facture",
    'impots',
    "mysearches",
    "paperhandle",
    'product',
    "transactions",
    "supplier",
    "commercial"
]
# Application definition


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",

]

ROOT_URLCONF = 'zimpot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "zimpot/templates/"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'facture.context_processors.last_invoice_id',
                'supplier.context_processors.last_supplier_invoice',

            ],
        },
    },
]

WSGI_APPLICATION = 'zimpot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'progestion',
#         "USER": 'kierko',
#         "PASSWORD": 'K@rie123',
#         "HOST": "localhost",
#         "POST": "5454"
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
STATIC_ROOT = BASE_DIR / "statistfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [BASE_DIR / "zimpot/static"]
# AUTH_USER_MODEL = "account.UsersBase"

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]

# TEMPLATES = [
#     {
#         'DIRS': [BASE_DIR / 'templates'], # new
#     },
# ]

# COMPRESS_ROOT = BASE_DIR / 'static'
# print(BASE_DIR)
# COMPRESS_ENABLED = True
#
# STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
"""
    identifiant
    dev
    &aéz"e'r(t-
"""
# /c/Users/Kierie/PycharmProjects/ProGestion/src