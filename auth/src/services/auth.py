from functools import lru_cache
from typing import Any
import uuid
from api.v1.exception import UserCreateException
from api.v1.schemas.auth import LoginForm, SingUpForm, UserOut
from core.config import settings
from core.jwt_auth import JWT, Tokens
from db.models.role import Role
from db.models.user import User
from db.models.user_role import UserRole
from db.models.user_oauth import UserOauth
from db.pg import get_session
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services.abstracts import AbstractAuth
from services.history import ServiceHistory
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()


class InvalidCredentials(Exception):
    pass


class InvalidRefreshToken(Exception):
    pass


class ServiceAuth(AbstractAuth):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
        self.jwt = JWT(settings.jwt_key)
        self.history = ServiceHistory(db_session)

    async def signup(self, form: SingUpForm) -> User | None:
        try:
            user_dto = jsonable_encoder(form)
            user = User(**user_dto)
            self.db_session.add(user)
            await self.db_session.commit()
        except Exception as e:
            raise UserCreateException("username already exists") from e
        await self.db_session.refresh(user)
        return user

    async def login(self, form: LoginForm, user_agent: str) -> Tokens:
        try:
            user: User = (
                (await self.db_session.execute(select(User).filter(User.username == form.username))).scalars().one()
            )
            if user:
                if user.check_password(form.password):
                    roles = (
                        (
                            await self.db_session.execute(
                                select(Role, UserRole)
                                .join(Role, UserRole.role_id == Role.id)
                                .filter(UserRole.user_id == user.id)
                                .distinct()
                            )
                        )
                        .scalars()
                        .all()
                    )
                    tokens = self.jwt.create(
                        {
                            'user': user.username,
                            'roles': [role.name for role in roles],
                        }
                    )
                    await self.history.add_record(user_agent, user.id)
                    return tokens
        except NoResultFound:
            raise InvalidCredentials('User name or password incorrect')

    async def refresh_tokens(self, token: str) -> Tokens:
        if not self.jwt.is_valid(token):
            raise InvalidRefreshToken

        payload = self.jwt.get_payload(token)

        return self.jwt.create(payload)

    async def convert_provider_to_user_tokens(self, provider: str, id_: str) -> Tokens:
        try:
            user = (
                (
                    await self.db_session.execute(
                        select(User, UserOauth)
                        .join(User, UserOauth.user_id == User.id)
                        .filter(UserOauth.oauth_name == provider, UserOauth.oauth_id == id_)
                        .distinct()
                    )
                )
                .scalars()
                .one()
            )
        except NoResultFound:

            user = await self.signup(
                SingUpForm(username=f'{provider}_{id_}', password=str(uuid.uuid4()), first_name='', last_name='')
            )
            user_oauth = UserOauth(user_id=user.id, oauth_name=provider, oauth_id=id_)
            self.db_session.add(user_oauth)
            await self.db_session.commit()

        return self.jwt.create(
            {
                'user': user.username,
                'roles': [],
            }
        )


class HasAccess:
    def __init__(self, roles: list[str]):
        self.roles = roles
        self.jwt = JWT(settings.jwt_key)

    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        if self.jwt.is_valid(credentials.credentials):
            if len(self.roles) == 0:
                return True
            payload = self.jwt.get_payload(credentials.credentials)
            roles = payload.get('roles', [])

            if set(self.roles).intersection(set(roles)):
                return True

        raise HTTPException(status_code=401, detail='Для просмотра необходимо произвести вход по адресу /login')


@lru_cache()
def get_service_auth(db_session: AsyncSession = Depends(get_session)) -> ServiceAuth:
    return ServiceAuth(
        db_session=db_session,
    )


# @lru_cache()
def get_token_payload(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, Any]:
    jwt: JWT = JWT(settings.jwt_key)
    return jwt.get_payload(credentials.credentials)


all_access = HasAccess([])
admin_access = HasAccess(['admin'])
