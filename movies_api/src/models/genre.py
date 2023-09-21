from pydantic import Field, UUID4

from models.base import Base


class Genre(Base):
    id: str = Field(default_factory=UUID4)
    name: str
    description: str | None


class Genres(Base):
    items: list[Genre] = []
