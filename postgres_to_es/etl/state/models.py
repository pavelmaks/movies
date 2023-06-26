import uuid
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, validator

from .base_storage import BaseStorage


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        return self.storage.retrieve_state().get(key)


class Movie(BaseModel):
    id: uuid.UUID
    imdb_rating: Optional[float] = Field(alias='rating')
    genre: list[str]
    title: str
    description: Optional[str]
    director: Optional[str]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    actors: List[dict[str, str]]
    writers: List[dict[str, str]]
    modified: datetime
