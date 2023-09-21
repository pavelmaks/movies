import json
from functools import lru_cache

from api.v1.exception import UserCreateException
from api.v1.schemas.auth import SingUpForm
from api.v1.schemas.user import UserOut
from db.models.role import Role
from db.models.user import User
from db.models.user_role import UserRole
from db.pg import get_session
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from services.abstracts import AbstractUser
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceUser(AbstractUser):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def user_history(self, payload) -> UserOut | None:
        user_dict = json.loads(payload.get('user'))
        user = UserOut(**user_dict)
        return user

    async def create(self, form: SingUpForm) -> User | None:
        try:
            user_dto = jsonable_encoder(form)
            user = User(**user_dto)
            self.db_session.add(user)
            await self.db_session.commit()
        except Exception as e:
            raise UserCreateException("username already exists") from e
        await self.db_session.refresh(user)
        return user

    async def roles(self, user_id) -> list[Role] | None:
        roles = (
            (
                await self.db_session.execute(
                    select(Role, UserRole).join(Role, UserRole.role_id == Role.id).filter(UserRole.user_id == user_id)
                )
            )
            .scalars()
            .all()
        )
        return roles

    async def add_role(self, user_id, role_id) -> list[Role] | None:
        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.db_session.add(user_role)
        await self.db_session.commit()
        return await self.roles(user_id)

    async def delete_role(self, user_id, role_id) -> list[Role] | None:
        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.db_session.delete(user_role)
        await self.db_session.execute(
            delete(UserRole).where((UserRole.user_id == user_id) & (UserRole.role_id == role_id))
        )
        await self.db_session.commit()
        return await self.roles(user_id)


@lru_cache()
def get_service_user(
    db_session: AsyncSession = Depends(get_session),
) -> ServiceUser:
    return ServiceUser(
        db_session=db_session,
    )
