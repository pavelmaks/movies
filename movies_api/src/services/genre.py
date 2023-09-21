import json
from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_scan
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre, Genres
from services.base_service import BaseService


class GenreService(BaseService):
    """Класс для работы с индексом genres"""
    async def get_all(
        self,
        query_params: str,
    ) -> Genres | None:
        """Получение полного списка жанров"""
        value = await self._value_from_cache(query_params)
        if value is None:
            genres = await self._get_genres_from_elastic()
            await self._put_value_to_cache(query_params, genres.json())
        else:
            genres = Genres(**json.loads(value))
        return genres

    async def _get_genres_from_elastic(self) -> Genres:
        """Получение списка жанров из elastic"""
        genres = Genres()
        try:
            async for doc in async_scan(self.elastic, index=self.index):
                genres.items.append(Genre(**doc['_source']))
        except NotFoundError:
            return genres
        return genres


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic, 'genres', Genre)
