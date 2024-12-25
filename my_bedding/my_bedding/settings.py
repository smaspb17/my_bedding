import os

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'debug_toolbar',
    "phonenumber_field",
    "mptt",
    "django_mptt_admin",
    "users.apps.UsersConfig",
    "shop.apps.ShopConfig",
    "cart.apps.CartConfig",
    "orders.apps.OrdersConfig",
    "coupons.apps.CouponsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1',]

ROOT_URLCONF = "my_bedding.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "my_bedding.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

CART_SESSION_ID = 'cart'

# PHONENUMBER_DEFAULT_REGION = 'RU'
# PHONENUMBER_DB_FORMAT = 'E164'  # Для хранения в международном формате (+7XXXXXXXXXX)
# PHONENUMBER_DEFAULT_FORMAT = 'E164'