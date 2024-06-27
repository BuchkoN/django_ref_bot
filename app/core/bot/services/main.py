import asyncio
import logging
from functools import lru_cache

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.exceptions import TelegramBadRequest
from app.core.bot.handlers.user import router as user_router
from app.core.bot.middlewares import TelegramLocaleMiddleware
from django.conf import settings


logger = logging.getLogger(__name__)
bot_event_loop = asyncio.new_event_loop()


async def run_bot() -> tuple[Bot, Dispatcher]:
    bot: Bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp: Dispatcher = Dispatcher(bot=bot)
    dp.update.outer_middleware(TelegramLocaleMiddleware())
    dp.include_router(user_router)
    try:
        await bot.set_webhook(settings.TELEGRAM_BOT_WEBHOOK_URL)
        logger.warning('Telegram Bot initialized')
    except TelegramBadRequest as e:
        logger.error(f'Telegram Bot webhook is not sets: {e}')
    return bot, dp


@lru_cache(maxsize=1)
def init_bot() -> tuple[Bot, Dispatcher]:
    asyncio.set_event_loop(bot_event_loop)
    return bot_event_loop.run_until_complete(run_bot())
