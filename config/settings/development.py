from .base import *
from .base import env

DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-rh3w890yi8bn8lkmv#d$%v_4-&adcukrpodm@ekm9%l7@1rrt9",
)

hosts = env(
    "DJANGO_ALLOWED_HOSTS", default="halfquiz.local localhost host.docker.internal"
)

ALLOWED_HOSTS = hosts.split(" ")

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
