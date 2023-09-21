import datetime as dt
from typing import Any

import jwt
from core.config import settings
from pydantic import BaseModel

ALGORITHM = 'HS256'


class AccessToken(BaseModel):
    access_token: str = ...


class RefreshToken(BaseModel):
    refresh_token: str = ...


class Tokens(AccessToken, RefreshToken):
    pass


class JWT(object):
    def __init__(
        self,
        key: str,
        algorithm: str = ALGORITHM,
        access_expire: int = settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        refresh_expire: int = settings.REFRESH_TOKEN_EXPIRE_SECONDS,
    ) -> None:
        self.key = key
        self.algorithm = algorithm
        self.access_expire = access_expire
        self.refresh_expire = refresh_expire

    def __create__(self, payload: dict[str, str], expire_in_seconds: int = 60) -> str:
        now = dt.datetime.utcnow()
        data: dict[str, str] = {
            'iat': now,
            'exp': now + dt.timedelta(seconds=expire_in_seconds),
        }
        data.update(payload)
        return jwt.encode(data, self.key, self.algorithm)

    def create(self, payload: dict[str, str]):
        return Tokens(
            access_token=self.__create__(payload, self.access_expire),
            refresh_token=self.__create__(payload, self.refresh_expire),
        )

    def get_payload(self, token: str) -> dict[str, Any] | None:
        return jwt.decode(token, self.key, [self.algorithm])

    def is_valid(self, token: str) -> bool:
        result = False
        try:
            payload = self.get_payload(token)
            result = all((isinstance(payload, dict), payload.get('exp', 0) > dt.datetime.utcnow().timestamp()))
        except Exception:
            pass
        return result
