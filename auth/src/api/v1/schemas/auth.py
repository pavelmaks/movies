import uuid

from pydantic import BaseModel


class SingUpForm(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str


class LoginForm(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    username: str
