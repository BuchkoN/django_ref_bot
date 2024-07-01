from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Update
from app.core.accounts.models import UserLanguageChoices
from app.core.accounts.repositories.repositories import UsersRepository
from django.utils import translation


class TelegramLocaleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        user_telegram_id = getattr(event, event.event_type).from_user.id
        user = await UsersRepository().get_user_by_telegram_id(telegram_id=user_telegram_id)
        language = user.language if user is not None else UserLanguageChoices.english
        with translation.override(language):
            return await handler(event, data)
