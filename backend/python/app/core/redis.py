import redis.asyncio as redis
from app.core.config import settings


class RedisManager:
    def __init__(self):
        self.redis: redis.Redis | None = None
    
    async def connect(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    async def disconnect(self):
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> str | None:
        return await self.redis.get(key) if self.redis else None
    
    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        return await self.redis.set(key, value, ex=ex) if self.redis else False
    
    async def delete(self, key: str) -> int:
        return await self.redis.delete(key) if self.redis else 0


redis_manager = RedisManager()