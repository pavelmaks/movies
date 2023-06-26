import os

from dotenv import load_dotenv
from pydantic import PostgresDsn, BaseSettings, Field

# load_dotenv()

class EtlSettings(BaseSettings):
    host: str = os.environ.get('EL_HOST') if os.environ.get('DOCKER_CONTAINER') == '1' else '127.0.0.1'
    port: int = os.environ.get('EL_PORT', 9200)

    class Config:
        env_file = '.env'


class PostgresSettings(BaseSettings):
    user: str = os.environ.get('POSTGRES_USER')
    password: str = os.environ.get('POSTGRES_PASSWORD')
    host: str = os.environ.get('DB_HOST') if os.environ.get('DOCKER_CONTAINER') == '1' else '127.0.0.1'
    port: int = os.environ.get('DB_PORT', 5432)
    database: str = os.environ.get('POSTGRES_DB')
    options: str = '-c search_path=content'

    class Config:
        env_file = '.env'

DSL = PostgresSettings().dict()
EL = EtlSettings().dict()
LAST_FILMWORK_KEY = 'last_filmwork_updated'
CHECK_DATA_TIMER = 1
