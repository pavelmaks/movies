import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float | None = Field(alias="rating")
    description: str | None
    modified: datetime
    genre: list[str]
    director: str
    actors_names: list[str]
    writers_names: list[str]
    actors: list[dict[str, str]]
    writers: list[dict[str, str]]


class Genre(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    modified: datetime


class PersonFilm(BaseModel):
    uuid: uuid.UUID
    roles: list[str]


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    modified: datetime
    films: list[PersonFilm]
