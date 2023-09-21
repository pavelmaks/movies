import uuid

from pydantic import BaseModel, ConfigDict


class UserOut(BaseModel):
    id: uuid.UUID
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserRole(BaseModel):
    user_id: uuid.UUID
    role_id: uuid.UUID
