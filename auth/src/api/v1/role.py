import uuid

from api.v1.http_methods import _response
from db.models import role as models
from db.pg import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from services.abstracts import AbstractRole, AbstractUser
from services.auth import admin_access
from services.role import get_service_role
from services.user import get_service_user
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .exception import RoleCreateException
from .schemas import role as schemas
from .schemas.role import RoleBaseSchema
from .schemas.user import UserRole

router = APIRouter()


@router.get('/',
    summary="Получение всех ролей",
    description="Получение списка ролей",
    response_description="")
async def get_roles(
    service_role: AbstractRole = Depends(get_service_role),
    limit: int = Query(10, title='Количество элементов', alias='size', le=100),
    page: int = Query(1, title='Номер страницы', alias='from', ge=1),
    search: str = '',
):
    skip = (page - 1) * limit
    roles = await service_role.get_roles(search, limit, skip)
    roles_items = [RoleBaseSchema(**item.__dict__) for item in roles]
    return _response(status.HTTP_200_OK, results=len(roles), roles=roles_items)


@router.post('/',
    status_code=status.HTTP_201_CREATED,
    summary="Создание роли",
    description="Добавление роли",
    response_description="")
async def create_role(
    payload: schemas.RoleCreateSchema,
    service_role: AbstractRole = Depends(get_service_role),
):
    try:
        new_role = await service_role.create_role(payload)
    except RoleCreateException:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Role already exists')
    return _response(status.HTTP_200_OK, results=new_role)


@router.patch('/{role_id}',
    summary="Обновление роли",
    description="Изменение данных роли",
    response_description="")
async def update_role(
    role_id: uuid.UUID,
    payload: schemas.RoleBaseSchema,
    service_role: AbstractRole = Depends(get_service_role),
    db_session: AsyncSession = Depends(get_session),
):
    db_role = (await db_session.execute(select(models.Role).filter(models.Role.id == role_id))).scalars().first()

    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No role with id: {role_id} found')
    update_data = payload.model_dump(exclude_unset=True)
    db_role = await service_role.update_role(role_id, update_data)
    return _response(status.HTTP_200_OK, role=db_role)


@router.get('/{role_id}',
    summary="Получение информации о роли",
    description="Описание роли",
    response_description="")
async def get_role(
    role_id: str,
    service_role: AbstractRole = Depends(get_service_role),
):
    db_role = await service_role.get_role(role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No role with id: {role_id} found')
    return _response(status.HTTP_200_OK, role=db_role)


@router.get('/user/{user_id}',
    summary="Получение информации о пользователе",
    description="Получение списка пользовательской методаты",
    response_description="")
async def get_user_roles(
    user_id: uuid.UUID,
    service_user: AbstractUser = Depends(get_service_user),
):
    roles = await service_user.roles(user_id)
    return _response(status.HTTP_200_OK, roles=roles)


@router.post('/user',
    summary="Добавление роли",
    description="Создание роли",
    response_description="",
    dependencies=[Depends(admin_access)])
async def add_user_role(
    user_role: UserRole,
    service_user: AbstractUser = Depends(get_service_user),
):
    roles = await service_user.add_role(user_role.user_id, user_role.role_id)
    return _response(status.HTTP_200_OK, roles=roles)


@router.delete('/user',
    summary="Удаление роли у пользователя",
    description="Деактивировать права пользователю",
    response_description="")
async def delete_user_role(
    user_role: UserRole,
    service_user: AbstractUser = Depends(get_service_user),
):
    roles = await service_user.delete_role(user_role.user_id, user_role.role_id)
    return _response(status.HTTP_200_OK, roles=roles)


@router.delete('/{role_id}',
    summary="Удаление роли",
    description="Деактивация роли")
async def delete_role(
    role_id: str,
    service_role: AbstractRole = Depends(get_service_role),
):
    db_role = await service_role.delete_role(role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No role with id: {role_id} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
