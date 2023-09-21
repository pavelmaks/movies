import json
from abc import ABC, abstractmethod

from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel
from redis.asyncio import Redis
from services.cache import RedisCache


class AbstractStorage(ABC):
    @abstractmethod
    def get_from_storage(self, **kwargs):
        pass

    @abstractmethod
    def search_from_storage(self, **kwargs):
        pass


class Storage(AbstractStorage):
    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.elastic = elastic

    async def check_elastic_connection(self) -> None:
        if not await self.elastic.ping():
            raise ConnectionError

    async def get_from_storage(self, index, query):
        await self.check_elastic_connection()
        return await self.elastic.get(index, query)

    async def search_from_storage(self, index, query):
        await self.check_elastic_connection()

        return await self.elastic.search(index=index, body=query)


class BaseService(RedisCache, Storage):
    """Базовый класс для работы с индексами"""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str, model: BaseModel):
        super().__init__(redis=redis)
        self.elastic = elastic
        self.index = index
        self.model = model

    async def get_by_id(self, obj_id: str, query_params: str) -> BaseModel | None:
        """Получение объекта по uuid"""
        obj = await self._value_from_cache(query_params)
        if not obj:
            obj = await self._get_obj_from_elastic(obj_id)
            if not obj:
                return None
            await self._put_value_to_cache(query_params, obj.json())
        else:
            obj = self.model(**json.loads(obj))
        return obj

    async def _get_obj_from_elastic(self, obj_id: str) -> BaseModel | None:
        """Запрос по uuid в elastic"""
        try:
            doc = await self.get_from_storage(index=self.index, query=obj_id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])
