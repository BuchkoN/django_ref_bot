from typing import (
    Any,
    Dict,
    Union,
)

from aiogram.filters import Filter
from aiogram.types import (
    Message,
    User as BotUser,
)
from app.core.accounts.repositories.repositories import UsersRepository


class FunnelPassedUserFilter(Filter):
    async def __call__(
            self,
            message: Message,
            event_from_user: BotUser
    ) -> Union[bool, Dict[str, Any]]:
        user = await UsersRepository().get_user_by_telegram_id(telegram_id=event_from_user.id)
        if user.is_funnel_passed:
            return {"user": user}
        return False
