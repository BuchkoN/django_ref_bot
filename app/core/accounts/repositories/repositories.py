from typing import Union

from aiogram.types import Chat
from django.contrib.auth import get_user_model


User = get_user_model()


async def get_or_create_user_from_telegram(chat: Chat) -> tuple[User, bool]:
    try:
        user = await User.objects.aget(telegram_id=chat.id)
        created = False
    except User.DoesNotExist:
        user = await User.objects.acreate(
            telegram_id=chat.id,
            username=f'TG_{chat.id}',
            telegram_username=chat.username,
        )
        created = True
    return user, created


async def get_user_by_telegram_id(telegram_id: int) -> Union[User, None]:
    try:
        return await User.objects.aget(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None
