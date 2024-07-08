"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from dataclasses import (
    dataclass,
    field,
)

from app.project.base.application import BaseASGILifespanApplication
from django.core.asgi import get_asgi_application
from django.core.handlers.asgi import ASGIHandler


@dataclass
class ASGILifespanApplication(BaseASGILifespanApplication):
    application: ASGIHandler = field(default_factory=get_asgi_application, kw_only=True)

    @staticmethod
    async def on_startup() -> None:
        from app.core.bot.services.main import init_bot
        await init_bot()

    @staticmethod
    async def on_shutdown() -> None:
        ...


django_settings = (
    f'app.project.settings.'
    f'{"local_settings" if os.environ.get("STAND_TYPE") == "DEV" else "settings"}'
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings)


application = ASGILifespanApplication()
