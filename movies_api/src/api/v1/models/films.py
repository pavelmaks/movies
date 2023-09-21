import uuid

from pydantic import BaseModel


class FilmDetail(BaseModel):
    id: uuid.UUID
    imdb_rating: float | None
    genre: list[str]
    title: str
    description: str | None
    director: list[str] | None
    actors_names: list[str] | None
    writers_names: list[str] | None
    actors: list[dict[str, str]]
    writers: list[dict[str, str]]


class Film(BaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float | None
