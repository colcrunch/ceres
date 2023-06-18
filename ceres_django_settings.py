import os

from dotenv import load_dotenv

if os.path.exists(".env.dev"):
    load_dotenv(".env.dev")
else:
    load_dotenv(".env")


ABSOLUTE_URL_OVERRIDES = {}

CSRF_TRUSTED_ORIGINS = ["http://localhost"]
CSRF_FAILURE_VIEW = "django.views.csrf.csrf_failure"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", None),
        "USER": os.getenv("DB_USER", None),
        "PASSWORD": os.getenv("DB_PASS", None),
        "HOST": os.getenv("DB_HOST", None),
        "PORT": "3306",
    }
}
DEFAULT_TABLESPACE = ""
DEFAULT_INDEX_TABLESPACE = ""
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
DATABASE_ROUTERS = []

MIGRATION_MODULES = {}
USE_TZ = "UTC"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

INSTALLED_APPS = [f"cogs.{ext}" for ext in os.getenv("EXTENSIONS", "").replace(" ", "").split(",")]

LOGGING = {}
LOGGING_CONFIG = {}

FORCE_SCRIPT_NAME = None
STATIC_URL = None
MEDIA_URL = None
TEMPLATES = []

LANGUAGE_CODE = "en-us"
USE_I18N = False

LANGUAGES_BIDI = []
LANGUAGES = []
SILENCED_SYSTEM_CHECKS = []
AUTH_USER_MODEL = 'auth.User'
