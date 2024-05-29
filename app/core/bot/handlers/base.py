from typing import Optional

from aiogram import Router
from app.core.bot.middlewares import TelegramLocaleMiddleware


class LocalizedRouter(Router):
    def __init__(self, *, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self.message.middleware(TelegramLocaleMiddleware())
