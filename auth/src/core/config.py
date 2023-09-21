import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='REDIS_', env_file='.env', env_file_encoding='utf-8', extra='ignore', case_sensitive=False
    )

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = 'Аутентификация и авторизация пользователей'
    jwt_key: str = Field(..., alias='JWT_KEY')
    # Настройки Redis
    REDIS_HOST: str = Field(..., alias='REDIS_HOST')
    REDIS_PORT: int = 6379

    # === JWT Tokens Expire time in seconds ===
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 300  # 5 minutes
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 604800  # 7 days

    GRPC_SERVER_ADDRESS: str = Field(..., alias='GRPC_SERVER_ADDRESS')
    GRPC_SERVER_PORT: int = Field(..., alias='GRPC_SERVER_PORT')
    ALGORITHM: str = Field('HS256', alias='ALGORITHM')
    AUTH_URL: str = Field(..., alias='AUTH_URL')
    DEBUG_ENGINE: bool = Field(..., alias='DEBUG_ENGINE')

    # Настройки Jaeger
    ENABLE_TRACER: bool = Field(True, env='ENABLE_TRACER')
    JAEGER_HOST: str = Field('jaeger', env='JAEGER_HOST')
    JAEGER_PORT: int = Field(6831, env='JAEGER_PORT')


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='POSTGRES_', env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )
    dbname: str = Field(..., alias='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = '127.0.0.1'
    port: int = 5432


class YandexSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='YANDEX_', env_file='env/auth.env', env_file_encoding='utf-8', extra='ignore'
    )
    REDIRECT_URI: str = ...
    CLIENT_ID: str = ...
    CLIENT_SECRET: str = ...
    URI: str = "https://oauth.yandex.com/authorize?response_type=code&client_id={}&redirect_uri={}"
    TOKEN_URI: str = 'https://oauth.yandex.com/token'
    INFO_URI: str = 'https://login.yandex.ru/info'


settings = Settings()
db_settings = DatabaseSettings()
yandex_settings = YandexSettings()
