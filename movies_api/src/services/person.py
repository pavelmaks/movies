import json
from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import FilmPerson, FilmsPerson, Person, Persons
from services.base_service import BaseService
from services.film import FilmService


class PersonService(BaseService):
    """Класс для работы с индексом persons"""

    async def get_films_by_id(
            self,
            person_id: str,
            query_params: str,
            film_service: FilmService
    ) -> FilmsPerson:
        """Получение фильмов по персоне"""
        films = FilmsPerson()
        value = await self._value_from_cache(query_params)
        if value is None:
            person = await self.get_by_id(person_id, query_params)
            if person:
                for film in person.films:
                    film_detail = await film_service.get_by_id(str(film.uuid), str(film.uuid))
                    films.items.append(FilmPerson(
                        id=film_detail.id,
                        title=film_detail.title,
                        imdb_rating=film_detail.imdb_rating
                    )
                    )
            await self._put_value_to_cache(query_params, films.json())
        return films

    async def get_all(
            self,
            query_params: str,
            page_size: int,
            page_number: int,
            sort: str | None = None,
            query: str | None = None,
    ) -> Persons | None:
        """Получение всех персон"""
        persons = Persons()
        value = await self._value_from_cache(query_params)

        if value is None:
            persons = await self._get_persons_from_elastic(
                sort=sort, query=query, page_number=page_number, page_size=page_size
            )
            await self._put_value_to_cache(query_params, persons.json())
        else:
            persons = Persons(**json.loads(value))

        return persons

    async def _get_persons_from_elastic(
            self,
            page_number: int,
            page_size: int,
            sort: str | None = None,
            query: str | None = None,
    ) -> Persons:
        """Получение всех персон из elastic"""
        body = {
            'from': (page_number - 1) * page_size,
            'size': page_size,
        }
        if sort:
            sort_field = sort[1:] if sort[:1] == '-' else sort
            sort_order = 'desc' if sort[:1] == '-' else 'asc'
            body.update({'sort': {sort_field: {"order": sort_order}}})

        if query:
            body.update(
                {'query': {'wildcard': {'full_name': {'value': f'*{query}*'}}}}
            )
        try:
            docs = await self.elastic.search(index=self.index, body=body)
        except NotFoundError:
            return Persons()

        return Persons(items=[Person(**doc['_source']) for doc in docs['hits']['hits']])


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic, 'persons', Person)
