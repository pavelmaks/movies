from http import HTTPStatus

from api.v1.models.films import Film, FilmDetail
from core.exceptions import FILM_NOT_FOUND
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/search',
    response_model=list[Film],
    summary="Найти фильмы",
    description="Найти фильмы",
    response_description="Список найденых фильмов",
)
async def films_search(
    request: Request,
    query: str | None = Query(None, title='Поисковая строка', alias='query'),
    page_size: int | None = Query(50, title='Пагинация "cколько элементов на странице"', alias='size', le=100),
    page_number: int | None = Query(1, title='Пагинация "номер страницы"', alias='from', ge=1),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    films = await film_service.get_all(
        query_params=f'{request.url.path}?{request.url.query}',
        query=query,
        page_size=page_size,
        page_number=page_number,
    )
    if not films:
        return []

    return [Film(**film.dict()) for film in films.items]


@router.get(
    '/{film_id}',
    response_model=FilmDetail,
    summary="Получить фильм по ID",
    description="Получить информацию по фильму по ID",
    response_description="Название и рейтинг фильма",
)
async def film_details(
    film_id: str,
    request: Request,
    film_service: FilmService = Depends(get_film_service),
) -> FilmDetail:
    film = await film_service.get_by_id(obj_id=film_id, query_params=f'{request.url.path}?{request.url.query}')
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return FilmDetail(**film.dict())


@router.get(
    '/',
    response_model=list[Film],
    summary="Получить все фильмы",
    description="Получить список фильмов",
    response_description="Список фильмов",
)
async def films(
    request: Request,
    sort: str | None = Query('title.raw', title='Сортировка по запросу', alias='sort_by'),
    page_size: int | None = Query(50, title='Пагинация "cколько элементов на странице"', alias='size'),
    page_number: int | None = Query(1, title='Пагинация "номер страницы"', alias='from'),
    genre: str | None = Query('Action', title='Жанр', alias='genre'),
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    films = await film_service.get_all(
        query_params=f'{request.url.path}?{request.url.query}',
        sort=sort,
        page_size=page_size,
        page_number=page_number,
        genre=genre,
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)

    return [Film(**film.dict()) for film in films.items]
