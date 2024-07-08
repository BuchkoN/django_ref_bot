from abc import abstractmethod
from dataclasses import dataclass

from django.core.handlers.asgi import ASGIHandler


@dataclass
class BaseASGILifespanApplication:
    application: ASGIHandler

    async def __call__(self, scope, receive, send) -> None:
        if scope['type'] == 'lifespan':
            await self.lifespan(scope, receive, send)
            return
        await self.application(scope, receive, send)

    @staticmethod
    @abstractmethod
    async def on_startup() -> None:
        ...

    @staticmethod
    @abstractmethod
    async def on_shutdown() -> None:
        ...

    async def lifespan(self, scope, receive, send) -> None:
        message = await receive()
        if message['type'] == 'lifespan.startup':
            await self.on_startup()
            await send({'type': 'lifespan.startup.complete'})
        elif message['type'] == 'lifespan.shutdown':
            await self.on_shutdown()
            await send({'type': 'lifespan.shutdown.complete'})
