import uuid
from typing import Any, Optional
from datetime import datetime

from pydantic import BaseModel

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
    title: str
    description: Optional[str]
    # creation_date: datetime
    rating: Optional[float]
    # film_type: str
    created: datetime
    modified: datetime
    # certificate: str
    # file_path: str
