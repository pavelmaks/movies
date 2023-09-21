from functools import lru_cache
from typing import List

from api.v1.exception import RoleCreateException
from db.models.role import Role
from db.pg import get_session
from fastapi import Depends
from services.abstracts import AbstractRole
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceRole(AbstractRole):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_roles(self, search, limit, skip) -> List[Role] | None:
        return (
            (
                await self.db_session.execute(
                    select(Role).filter(Role.name.contains(search)).limit(limit).offset(skip)
                )
            )
            .scalars()
            .all()
        )

    async def update_role(self, role_id, update_data) -> Role | None:
        db_role = (
            (
                await self.db_session.execute(
                    update(Role).where(Role.id == role_id).values(update_data).returning(Role)
                )
            )
            .scalars()
            .first()
        )
        if db_role:
            await self.db_session.commit()
        return db_role

    async def get_role(self, role_id) -> str | None:
        return (await self.db_session.execute(select(Role).filter(Role.id == role_id))).scalars().first()

    async def delete_role(self, role_id) -> Role | None:
        db_role = (await self.db_session.execute(select(Role).filter(Role.id == role_id))).scalars().first()
        if db_role:
            await self.db_session.execute(delete(Role).where(Role.id == role_id))
            await self.db_session.commit()
        return db_role

    async def create_role(self, payload) -> str | None:
        try:
            new_role = Role(**payload.model_dump())
            self.db_session.add(new_role)
            await self.db_session.commit()
        except Exception as e:
            raise RoleCreateException("role already exists") from e
        await self.db_session.refresh(new_role)
        return new_role


@lru_cache()
def get_service_role(
        db_session: AsyncSession = Depends(get_session)
) -> ServiceRole:
    return ServiceRole(
        db_session=db_session,
    )
