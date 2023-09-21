import uuid

from pydantic import BaseModel


class PersonFilm(BaseModel):
    uuid: uuid.UUID
    roles: list[str]


class Person(BaseModel):
    id: uuid.UUID
    full_name: str
    films: list[PersonFilm] | None


class FilmPerson(BaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float | None
