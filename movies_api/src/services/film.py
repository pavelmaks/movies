import json
from functools import lru_cache

from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film, Films
from redis.asyncio import Redis
from services.base_service import BaseService


class FilmService(BaseService):
    """Класс для работы с индексом movies"""

    async def get_all(
        self,
        query_params: str,
        page_size: int,
        page_number: int,
        genre: str | None = None,
        sort: str | None = None,
        query: str | None = None,
    ) -> Films | None:
        """Получение списка фильмов с фильтрацией"""
        films = Films()
        value = await self._value_from_cache(query_params)

        if value is None:
            films = await self._get_films_from_elastic(
                sort=sort, query=query, page_number=page_number, page_size=page_size, genre=genre
            )
            await self._put_value_to_cache(query_params, films.json())
        else:
            films = Films(**json.loads(value))

        return films

    async def _get_films_from_elastic(
        self,
        page_number: int,
        page_size: int,
        genre: str | None = None,
        sort: str | None = None,
        query: str | None = None,
    ) -> Films:
        """Получение списка фильмов с фильтрацией из elastic"""
        body = {
            'from': (page_number - 1) * page_size,
            'size': page_size,
        }
        if sort:
            sort_field = sort[1:] if sort[:1] == '-' else sort
            sort_order = 'desc' if sort[:1] == '-' else 'asc'
            body.update({'sort': {sort_field: {"order": sort_order}}})

        if query:
            body.update({'query': {'wildcard': {'title': {'value': f'*{query}*'}}}})
        if genre:
            body.update({'query': {'bool': {'filter': {'wildcard': {'genre': {'value': f'*{genre}*'}}}}}})

        try:
            # docs = await self.elastic.search(index=self.index, body=body)
            docs = await self.search_from_storage(index=self.index, query=body)

        except NotFoundError:
            return Films()

        return Films(items=[Film(**doc['_source']) for doc in docs['hits']['hits']])


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic, 'movies', Film)
