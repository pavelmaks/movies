from models.base import Base
from pydantic import UUID4, Field


class Film(Base):
    id: str = Field(default_factory=UUID4)
    imdb_rating: float | None
    genre: list[str]
    title: str
    description: str | None
    director: str | None
    actors_names: list[str] | None
    writers_names: list[str] | None
    actors: list[dict[str, str]]
    writers: list[dict[str, str]]


class Films(Base):
    items: list[Film] = []
