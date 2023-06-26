import os

from dotenv import load_dotenv

load_dotenv()

DSL = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('DB_HOST') if os.environ.get('DOCKER_CONTAINER') == '1' else '127.0.0.1',
    'port': os.environ.get('DB_PORT', 5432),
    'options': '-c search_path=content',
}

EL = {
    'host': os.environ.get('EL_HOST') if os.environ.get('DOCKER_CONTAINER') == '1' else '127.0.0.1',
    'port': os.environ.get('EL_PORT', 9200),
}

LAST_FILMWORK_KEY = 'last_filmwork_updated'
