from api.v1.http_methods import _response
from fastapi import APIRouter, Depends, Query
from services.auth import admin_access
from services.history import get_service_history
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

router = APIRouter()


@router.get(
    '/',
    summary='Просмотр истории авторизации пользователей',
    description='Список историй входа в систему',
    dependencies=[Depends(admin_access)],
)
async def history(
    history_service: AsyncSession = Depends(get_service_history),
    limit: int = Query(10, title='Количество элементов', alias='size', le=100),
    page: int = Query(1, title='Номер страницы', alias='from', ge=1),
    search: str = '',
):
    skip = (page - 1) * limit
    history = await history_service.history(limit, skip)
    return _response(status.HTTP_200_OK, results=len(history), history=history)
