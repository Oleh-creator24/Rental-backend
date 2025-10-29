import os
import sys
from pathlib import Path
from config.logging_setup import logger
from datetime import timedelta

# ── Загрузка .env ──────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

# ----------------------------------------------------------------------------- #
# BASE DIR
# ----------------------------------------------------------------------------- #
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ----------------------------------------------------------------------------- #
# SECURITY / DEBUG
# ----------------------------------------------------------------------------- #
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-xq=t%edyvu=z_2=q0q0yvds@a^qnpz!4*qe40g)az7jqni_dt8"
)

DEBUG = os.getenv("DEBUG", "1") in ("1", "true", "True")

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if h.strip()
]

# ----------------------------------------------------------------------------- #
# APPLICATIONS
# ----------------------------------------------------------------------------- #
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Utils
    "django_extensions",
    "django_filters",

    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # Local apps
    "users",
    "listings",
    "bookings",
    "reviews",
    "stats",
    "locations",
]

AUTH_USER_MODEL = "users.User"

# ----------------------------------------------------------------------------- #
# MIDDLEWARE / URLCONF / WSGI
# ----------------------------------------------------------------------------- #
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",           # ✅ ВАЖНО: перед SessionMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.config.urls"

# ----------------------------------------------------------------------------- #
# CORS (для Swagger и Docker)
# ----------------------------------------------------------------------------- #
CORS_ALLOW_ALL_ORIGINS = True  # ✅ Разрешаем все источники (удобно для демонстрации)

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "accept",
    "origin",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

# ----------------------------------------------------------------------------- #
# TEMPLATES
# ----------------------------------------------------------------------------- #
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "src" / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

# ----------------------------------------------------------------------------- #
# DATABASE (MySQL / PostgreSQL)
# ----------------------------------------------------------------------------- #
DB_ENGINE = os.getenv("DB_ENGINE", "mysql").lower()

if DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "rental"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DATABASE", "rental"),
            "USER": os.getenv("MYSQL_USER", "rental"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", "rental"),
            "HOST": os.getenv("MYSQL_HOST", "db"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'"
            },
        }
    }

if "test" in sys.argv or "pytest" in sys.argv:
    print("⚙️ Using main DB for tests (no CREATE DATABASE).")

# ----------------------------------------------------------------------------- #
# PASSWORD VALIDATION
# ----------------------------------------------------------------------------- #
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ----------------------------------------------------------------------------- #
# INTERNATIONALIZATION
# ----------------------------------------------------------------------------- #
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ----------------------------------------------------------------------------- #
# STATIC & MEDIA FILES
# ----------------------------------------------------------------------------- #
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "src" / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------------------------------------------------------- #
# REST FRAMEWORK / JWT / DOCS
# ----------------------------------------------------------------------------- #
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "config.pagination.DefaultPagination",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Rental Backend API",
    "DESCRIPTION": "API сервиса аренды жилья с бронированиями, отзывами и авторизацией JWT.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,

    "TAGS": [
        {"name": "Users", "description": "Работа с пользователями"},
        {"name": "Auth", "description": "Авторизация и токены"},
        {"name": "Stats", "description": "Статистика просмотров и запросов"},
        {"name": "Listings", "description": "Объявления"},
        {"name": "Bookings", "description": "Бронирования"},
        {"name": "Reviews", "description": "Отзывы"},
    ],
}

# ----------------------------------------------------------------------------- #
# EMAIL CONFIGURATION
# ----------------------------------------------------------------------------- #
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "1") in ("1", "true", "True")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "webmaster@localhost")

# --- TEST SETTINGS ---
if any(cmd in sys.argv[0] or cmd in sys.argv for cmd in ["test", "pytest"]):
    print("⚙️ Using main DB for tests (no CREATE DATABASE).")
    DATABASES["default"]["TEST"] = {"MIRROR": "default"}
