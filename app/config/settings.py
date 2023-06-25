import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include
load_dotenv()
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# else:
#     raise Exception('Нет .env файла')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')


# Application definition

include('components/application_definition.py')


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

include('components/database.py',)


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

include('components/password_validation.py',)

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

include('components/internationalization.py',)

# Logging SQL Queries
include('components/logging.py',)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
