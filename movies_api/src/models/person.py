from pydantic import Field, UUID4

from models.base import Base


class PersonFilm(Base):
    uuid: str = Field(default_factory=UUID4)
    roles: list[str]


class Person(Base):
    id: str = Field(default_factory=UUID4)
    full_name: str
    films: list[PersonFilm]


class Persons(Base):
    items: list[Person] = []


class FilmPerson(Base):
    id: str = Field(default_factory=UUID4)
    title: str
    imdb_rating: float | None


class FilmsPerson(Base):
    items: list[FilmPerson] = []
