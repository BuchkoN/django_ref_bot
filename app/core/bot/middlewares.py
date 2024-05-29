from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from app.core.accounts.models import UserLanguageChoices
from app.core.accounts.repositories.repositories import get_user_by_telegram_id
from django.utils import translation


class TelegramLocaleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = await get_user_by_telegram_id(event.chat.id)
        language = user.language if user is not None else UserLanguageChoices.english
        translation.activate(language)
        return await handler(event, data)
