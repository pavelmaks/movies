from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request, Query

from api.v1.models.persons import Person, FilmPerson
from core.exceptions import PERSON_NOT_FOUND
from services.film import FilmService, get_film_service
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    '/search',
    response_model=list[Person],
    summary="Найти персон",
    description="Найти персон",
    response_description="Список найденых персон",
)
async def persons_search(
        query: str,
        request: Request,
        page_size: int | None = Query(50, title='Пагинация "cколько элементов на странице"', alias='size'),
        page_number: int | None = Query(1, title='Пагинация "номер страницы"', alias='from'),
        person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    persons = await person_service.get_all(
        query_params=f'{request.url.path}?{request.url.query}',
        query=query,
        page_size=page_size,
        page_number=page_number,
    )
    if not persons:
        return []

    return [Person(**person.dict()) for person in persons.items]


@router.get(
    '/{person_id}',
    response_model=Person,
    summary="Получить персону по ID",
    description="Получить информацию по персоне по ID",
    response_description="Полное имя",
)
async def person_details(
        person_id: str,
        request: Request,
        person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id, query_params=f'{request.url.path}?{request.url.query}')
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return Person(id=person.id, full_name=person.full_name, films=person.films)


@router.get(
    '/{person_id}/films',
    response_model=list[FilmPerson],
    summary="Получить фильмы по персоне",
    description="Получить информацию фильмам по персоне",
    response_description="Фильмы",
)
async def films_on_person(
        person_id: str,
        request: Request,
        person_service: PersonService = Depends(get_person_service),
        film_service: FilmService = Depends(get_film_service)
) -> list[FilmPerson]:
    films = await person_service.get_films_by_id(
        person_id=person_id,
        query_params=f'{request.url.path}?{request.url.query}',
        film_service=film_service
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND)
    return [FilmPerson(**film.dict()) for film in films.items]
