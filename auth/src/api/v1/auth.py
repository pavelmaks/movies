from typing import Annotated

from core.jwt_auth import Tokens
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_limiter.depends import RateLimiter
from services.auth import InvalidCredentials, InvalidRefreshToken, get_service_auth
from sqlalchemy.ext.asyncio import AsyncSession

from .exception import UserCreateException
from .schemas.auth import LoginForm, SingUpForm
from .schemas.user import UserOut

security = HTTPBearer()

router = APIRouter()


@router.post(
    '/singup',
    response_model=UserOut,
    summary="Регистрация пользователя",
    description="Создание профиля для входа в систему",
    response_description="",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))]
)
async def signup(form: SingUpForm, service_auth: AsyncSession = Depends(get_service_auth)) -> UserOut:
    try:
        user = await service_auth.signup(form)
    except UserCreateException:
        raise HTTPException(status_code=401, detail='username already exists')
    return user


@router.post(
    '/login',
    response_model=Tokens,
    summary="Авторизация пользователя",
    description="Вход в систему",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))]
)
async def login(
    form: LoginForm,
    service_auth: AsyncSession = Depends(get_service_auth),
    user_agent: Annotated[str | None, Header()] = None,
) -> Tokens:
    try:
        return await service_auth.login(form, user_agent)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail='invalid username or password')


@router.delete(
    '/logout',
    summary="Выход из учетной записи",
    description="Выход из системы",
)
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)) -> None:
    return None


@router.post(
    '/refresh',
    response_model=Tokens,
    summary="Обновление токена",
    description="Обновить время жизни существующего токена",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))]
)
async def refresh(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service_auth: AsyncSession = Depends(get_service_auth),
) -> Tokens:
    try:
        return await service_auth.refresh_tokens(credentials.credentials)
    except InvalidRefreshToken:
        HTTPException(status_code=401, detail='refresh token is not valid')
