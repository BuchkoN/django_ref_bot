import json
import logging

from aiogram.types import Update
from app.api.utils import telegram_webhook_verify
from app.core.bot.services.main import init_bot
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseNotAllowed,
)
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


@csrf_exempt
async def telegram(request: HttpRequest):
    if request.method != 'POST' or not telegram_webhook_verify(request):
        logger.warning(
            f'Unexpected request to telegram webhook from '
            f'{request.headers.get("X-Forwarded-For")}'
        )
        return HttpResponseNotAllowed(permitted_methods=['POST'])

    bot, dp = await init_bot()
    upd = Update(**json.loads(request.body))
    await dp.feed_update(bot, upd)
    return HttpResponse(status=200)
