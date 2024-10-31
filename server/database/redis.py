import os

from redis import asyncio as aioredis


class TokenRepository:
    def __init__(self) -> None:
        self.red = aioredis.from_url(f"redis://{os.getenv('REDIS')}:6379/0", encoding='utf8',
                                     decode_responses=True)

    # Создание refresh token в БД
    async def set_token(self, key: str, item: str, expire_time: int = 60*24*30) -> None:
        await self.red.set(key, item, expire_time)

    # Получение refresh token из БД
    async def get_token(self, key: str) -> str | None:
        result = await self.red.get(key)
        return result
