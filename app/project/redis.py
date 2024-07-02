from redis.asyncio.client import Redis as AsyncRedis


class AsyncRedisClient:
    def __new__(cls, url: str, *args, **kwargs):
        return AsyncRedis.from_url(url=url)
