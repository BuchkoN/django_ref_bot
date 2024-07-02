from django.conf import settings
from redis.asyncio.client import Redis as AsyncRedis


class FSMRedisClient:
    def __new__(cls, *args, **kwargs):
        return AsyncRedis.from_url(url=settings.TELEGRAM_REDIS_FSM_URL)
