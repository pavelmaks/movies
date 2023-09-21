from abc import ABC, abstractmethod

from redis.asyncio import Redis


class AbstractCache(ABC):
    @abstractmethod
    def _value_from_cache(self, key: str) -> str | None:
        """Функция для получения данных"""
        pass

    @abstractmethod
    def _put_value_to_cache(self, key: str, obj: str) -> None:
        """Функция для кэширования данных"""
        pass


class RedisCache(AbstractCache):
    """Класс для реализации кэша в Redis"""

    BASE_CACHE_EXPIRE_IN_SECONDS = 60 * 5

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def _value_from_cache(self, key: str) -> str | None:
        """Функция для получения данных"""
        data = await self.redis.get(key)
        if not data:
            return None
        return data

    async def _put_value_to_cache(self, key: str, obj: str) -> None:
        """Функция для кэширования данных"""
        await self.redis.set(key, obj, self.BASE_CACHE_EXPIRE_IN_SECONDS)
