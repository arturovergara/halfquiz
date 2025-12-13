from .base import *
from .base import env

SECRET_KEY = env("DJANGO_SECRET_KEY")

hosts = env(
    "DJANGO_ALLOWED_HOSTS", default="halfquiz.local localhost host.docker.internal"
)
ALLOWED_HOSTS = hosts.split(" ")

CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS]

# Database
DATABASE_DIR = BASE_DIR.parent / "sqlite-data"
DATABASES["default"]["NAME"] = DATABASE_DIR / "db.sqlite3"  # noqa: F405
CONN_MAX_AGE = 0

# Admin
ADMIN_URL = env("DJANGO_ADMIN_URL")

# Security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)
