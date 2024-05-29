import asyncio
import json
import logging

from aiogram.types import Update
from app.api.utils import telegram_webhook_verify
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


@csrf_exempt
def telegram(request: HttpRequest):
    try:
        from app.core.bot.services.main import bot, bot_event_loop, dp  # isort: skip
    except ImportError:
        return HttpResponseForbidden()

    if request.method == 'POST' and telegram_webhook_verify(request):
        asyncio.set_event_loop(bot_event_loop)
        upd = Update(**json.loads(request.body))
        bot_event_loop.run_until_complete(dp.feed_update(bot, upd))
        return HttpResponse(status=200)
    logger.warning(
        f'Unexpected request to telegram webhook from '
        f'{request.headers.get("X-Forwarded-For")}'
    )
    return HttpResponseNotAllowed(permitted_methods=['POST'])