# """Development settings."""

from .base import *  # NOQA
from .base import env, env_aux

# Base
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

RENDER_EXTERNAL_HOSTNAME = env_aux.get('RENDER_EXTERNAL_HOSTNAME', None)

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS += [RENDER_EXTERNAL_HOSTNAME]


# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# django-extensions
# INSTALLED_APPS += ['django_extensions']  # noqa F405
