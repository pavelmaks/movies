import os

if os.getenv('DOCKER_CONTAINER'):
    POSTGRES_HOST = os.environ.get('DB_HOST')
else:
    POSTGRES_HOST = '127.0.0.1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': POSTGRES_HOST,
        'PORT': os.environ.get('DB_PORT', 5432),
        'OPTIONS': {
            # Нужно явно указать схемы, с которыми будет работать приложение.
            'options': '-c search_path=public,content'
        },
    }
}
