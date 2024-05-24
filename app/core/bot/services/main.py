import asyncio

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.exceptions import TelegramBadRequest
from django.conf import settings


async def init_bot(token: str, webhook_url: str) -> tuple[Bot, Dispatcher]:
    bot: Bot = Bot(token=token)
    dp: Dispatcher = Dispatcher(bot=bot)
    await bot.set_webhook(webhook_url)
    return bot, dp


try:
    bot_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_event_loop)
    bot, dp = bot_event_loop.run_until_complete(init_bot(
        settings.TELEGRAM_BOT_TOKEN,
        settings.TELEGRAM_BOT_WEBHOOK_URL
    ))
except TelegramBadRequest:
    pass
