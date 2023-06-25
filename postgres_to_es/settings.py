import os

from dotenv import load_dotenv
load_dotenv()
# dotenv_path = os.path.join(os.getcwd(), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     raise Exception('Нет .env файла')

DSL = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('DB_HOST') if os.environ.get('DOCKER_CONTAINER') == '1' else '127.0.0.1',
    'port': os.environ.get('DB_PORT', 5432),
    'options': '-c search_path=content',
}

STATE_KEY = 'last_movies_updated'
