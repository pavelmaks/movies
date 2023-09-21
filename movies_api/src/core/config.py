import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field('Фильмопоиск', env='PROJECT_NAME')
    # Настройки Redis
    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: int = Field(6379, env='REDIS_PORT')
    # Настройки Elasticsearch
    ELASTIC_HOST: str = Field('http://127.0.0.1', env='ES_HOST')
    ELASTIC_PORT: int = Field(9200, env='ES_PORT')
    # Настройки Jaeger
    ENABLE_TRACER: bool = Field(True, env='ENABLE_TRACER')
    JAEGER_HOST: str = Field('jaeger', env='JAEGER_HOST')
    JAEGER_PORT: int = Field(6831, env='JAEGER_PORT')

    grpc_server_address: str = Field('grpc_server', env='GRPC_SERVER_ADDRESS')
    grpc_server_port: int = Field(50051, env='GRPC_SERVER_PORT')

    class Config:
        env_file = '.env'


settings = Settings()
