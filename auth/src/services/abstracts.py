import uuid
from abc import ABC, abstractmethod
from typing import List

from api.v1.schemas.auth import LoginForm, SingUpForm
from api.v1.schemas.user import UserOut
from core.jwt_auth import Tokens
from db.models.history import History
from db.models.role import Role
from db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractUser(ABC):
    @abstractmethod
    async def user_history(self, payload) -> UserOut | None:
        pass

    @abstractmethod
    async def create(self, form: SingUpForm) -> UserOut | None:
        pass

    @abstractmethod
    async def roles(self, user_id: uuid.UUID) -> list[Role] | None:
        pass

    @abstractmethod
    async def add_role(self, user_id, role_id) -> list[Role] | None:
        pass

    @abstractmethod
    async def delete_role(self, user_id, role_id) -> list[Role] | None:
        pass


class AbstractRole(ABC):
    @abstractmethod
    async def get_roles(self, search, limit, skip) -> List[Role] | None:
        pass

    @abstractmethod
    async def update_role(self, role_id, update_data) -> Role | None:
        pass

    @abstractmethod
    async def get_role(self, role_id) -> str | None:
        pass

    @abstractmethod
    async def delete_role(self, role_id) -> Role | None:
        pass


class AbstractAuth(ABC):
    @abstractmethod
    async def signup(self, form: SingUpForm) -> User | None:
        pass

    @abstractmethod
    async def login(self, form: LoginForm) -> Tokens:
        pass

    @abstractmethod
    async def refresh_tokens(self, token: str) -> Tokens | None:
        pass


class AbstractHistory(ABC):
    @abstractmethod
    def add_record(self, agent: str) -> History | None:
        pass

    @abstractmethod
    def list_records(self, page: int, size: int) -> list[History] | None:
        pass


class AbstractProvider(ABC):
    def __init__(self, service_auth: AbstractAuth) -> None:
        self.service_auth = service_auth

    @abstractmethod
    def login(self, provider: str):
        pass

    @abstractmethod
    def callback(self):
        pass
