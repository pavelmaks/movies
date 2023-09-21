import logging
from logging.handlers import RotatingFileHandler

from pydantic import BaseSettings, Field

STATE_MOVIE_KEY = 'last_movies_updated'
STATE_GENRES_KEY = 'last_genres_updated'
STATE_PERSONES_KEY = 'last_persons_updated'

FETCH_BY = 100

logger_backoff = logging.getLogger('backoff')
logger = logging.getLogger('etl')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler('logs/etl.log', maxBytes=20_000_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger_backoff.addHandler(fh)


class DatabaseSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...

    class Config:
        env_prefix = 'postgres_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ESSettings(BaseSettings):
    host: str = ...

    class Config:
        env_prefix = 'es_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


database_settings = DatabaseSettings()
es_settings = ESSettings()
