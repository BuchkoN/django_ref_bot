import asyncio
import json

from aiogram.types import Update
from app.api.utils import telegram_webhook_verify
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def telegram(request: HttpRequest):
    try:
        from app.core.bot.services.main import (
            bot,
            bot_event_loop,
            dp,
        )
    except ImportError:
        return HttpResponse(status=404)

    if request.method == 'POST' and telegram_webhook_verify(request):
        asyncio.set_event_loop(bot_event_loop)
        upd = Update(**json.loads(request.body))
        bot_event_loop.run_until_complete(dp.feed_update(bot, upd))
        return HttpResponse(status=200)
    return HttpResponse(status=404)
