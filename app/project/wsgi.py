"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


django_settings = (
    f'app.project.settings.'
    f'{"local_settings" if os.environ.get("STAND_TYPE") == "DEV" else "settings"}'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings)

application = get_wsgi_application()
