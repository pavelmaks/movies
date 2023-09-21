import uuid
from typing import Any

from api.v1.schemas.user import UserOut
from db.pg import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from services.abstracts import AbstractHistory, AbstractUser
from services.auth import all_access, get_token_payload
from services.history import get_service_history
from services.user import get_service_user
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas.role import RoleBaseSchema

router = APIRouter()


@router.get(
    '/profile',
    response_model=UserOut,
    summary="Вывод информации о пользователе",
    description="Вывод методанных пользователя",
    dependencies=[Depends(all_access)],
)
async def user() -> UserOut:
    return UserOut(id='ee3a81e3-e130-4f7f-94fb-62cf4ec7a1c7', username='testuser')


@router.get(
    '/history',
    summary="История авторизации пользователя",
    description="История входа в систему конкретного пользователя",
    dependencies=[Depends(all_access)],
)
async def user_history(
    service_user: AbstractUser = Depends(get_service_user),
    service_history: AbstractHistory = Depends(get_service_history),
    payload: dict[str, Any] = Depends(get_token_payload),
):
    user = await service_user.user_history(payload)
    history_list = await service_history.list_records(1, 100, user.id)

    return {'status': 'success', 'results': len(history_list), 'history': history_list}


@router.get(
    '/{user_id}/role',
    response_model=UserOut,
    summary="Просмотр ролей пользователя",
    description="Просмотр ролей конкретного пользователя",
    dependencies=[Depends(all_access)],
)
async def list_roles(
    user_id: uuid.UUID, payload: RoleBaseSchema, db_session: AsyncSession = Depends(get_session)
) -> UserOut:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail='Method not implemented')


@router.post(
    '/{user_id}/role',
    response_model=UserOut,
    summary="Добавление роли пользователю",
    description="Добавление роли конкретному пользователю",
    dependencies=[Depends(all_access)],
)
async def add_role(
    user_id: uuid.UUID, payload: RoleBaseSchema, db_session: AsyncSession = Depends(get_session)
) -> UserOut:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail='Method not implemented')


@router.delete(
    '/{user_id}/role',
    response_model=UserOut,
    summary="Удаление роли у пользователя",
    description="Удаление роли конкретного опльзователя",
    dependencies=[Depends(all_access)],
)
async def delete_role(
    user_id: uuid.UUID, payload: RoleBaseSchema, db_session: AsyncSession = Depends(get_session)
) -> UserOut:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail='Method not implemented')
