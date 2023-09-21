from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from api.v1.models.genres import Genre
from core.exceptions import GENRE_NOT_FOUND
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary="Получить жанр по ID",
    description="Получить информацию по жанру по ID",
    response_description="Название жанра",
)
async def genre_details(
        request: Request,
        genre_id: str,
        genre_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(
        obj_id=genre_id,
        query_params=f'{request.url.path}?{request.url.query}'
    )
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    return Genre(id=genre.id, name=genre.name)


@router.get(
    '/',
    response_model=list[Genre],
    summary="Получить список жанров",
    description="Получить список жанров",
    response_description="Список жанров",
)
async def genres_list(
        request: Request,
        genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:
    genres = await genre_service.get_all(query_params=f'{request.url.path}?{request.url.query}')
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND)
    return [Genre(**genre.dict()) for genre in genres.items]
