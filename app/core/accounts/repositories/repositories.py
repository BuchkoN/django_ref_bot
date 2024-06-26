from dataclasses import (
    dataclass,
    field,
)

from aiogram.types import Chat
from app.project.base.repositories import BaseRepositoryDjango
from django.contrib.auth import get_user_model
from django.db.models import Manager


User = get_user_model()


@dataclass
class UsersRepository(BaseRepositoryDjango):
    manager: Manager = field(default=User.objects, kw_only=True)

    async def get_or_create_user_from_telegram_chat(self, chat: Chat) -> tuple[User, bool]:
        try:
            user = await self.manager.aget(telegram_id=chat.id)
            created = False
        except User.DoesNotExist:
            user = await self.manager.acreate(
                telegram_id=chat.id,
                username=f'TG_{chat.id}',
                telegram_username=chat.username,
            )
            created = True
        return user, created

    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.manager.filter(telegram_id=telegram_id).afirst()

    async def get_user_by_oid(self, oid: str) -> User | None:
        return await self.manager.filter(oid=oid).afirst()
