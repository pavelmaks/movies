import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.environ.get('DEBUG', False) == 'True'

JWT_KEY = os.environ.get('JWT_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

GRPC_SERVER_URL = f'{os.environ.get("GRPC_SERVER_ADDRESS")}:{os.environ.get("GRPC_SERVER_PORT")}'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies.apps.MoviesConfig',
    'customauth.apps.CustomauthConfig',
    'rangefilter',
    'django_extensions',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    INTERNAL_IPS = ['127.0.0.1', ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:8080']
AUTH_USER_MODEL = "customauth.User"

AUTHENTICATION_BACKENDS = [
    'customauth.authentication.CustomBackend',
    # 'django.contrib.auth.backends.ModelBackend',
]
