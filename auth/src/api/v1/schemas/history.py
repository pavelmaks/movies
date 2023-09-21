from datetime import datetime

from pydantic import BaseModel


class HistoryItem(BaseModel):
    auth_time: datetime
    user_agent: str


class History(BaseModel):
    items: list[HistoryItem]
