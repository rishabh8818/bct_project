"""
ASGI config for nit_library project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nit_library.settings')

application = get_asgi_application()
# CSRF and Session Settings
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = True
