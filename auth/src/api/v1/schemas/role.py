import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RoleCreateSchema(BaseModel):
    name: str


class RoleBaseSchema(BaseModel):
    id: uuid.UUID | None = None
    name: str
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class ListRoleResponse(BaseModel):
    status: str
    results: int
    roles: list[RoleBaseSchema]
