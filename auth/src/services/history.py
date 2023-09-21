import uuid
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.history import History
from db.pg import get_session
from services.abstracts import AbstractHistory


class ServiceHistory(AbstractHistory):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def add_record(self, agent: str, user_id: uuid.UUID) -> History | None:
        history = History(user_id=user_id, agent=agent)
        self.db_session.add(history)
        await self.db_session.commit()
        await self.db_session.refresh(history)
        return history

    async def list_records(self, page: int, size: int, user_id: uuid.UUID) -> list[History] | None:
        skip = (page - 1) * size

        history = (
            (
                await self.db_session.execute(
                    select(History).filter(History.user_id == user_id).limit(size).offset(skip)
                )
            )
            .scalars()
            .all()
        )

        return history

    async def history(self, limit, skip):
        return (
            (
                await self.db_session.execute(
                    select(History)
                    .limit(limit)
                    .offset(skip)
                )
            )
            .scalars()
            .all()
        )


@lru_cache()
def get_service_history(
        db_session: AsyncSession = Depends(get_session),
) -> ServiceHistory:
    return ServiceHistory(
        db_session=db_session,
    )
