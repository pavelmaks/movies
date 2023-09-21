#!/usr/bin/env bash

python manage.py collectstatic
apt-get update
apt-get -y install gettext
python manage.py makemessages -l en -l ru
python manage.py compilemessages -l en -l ru

/opt/app/uwsgi/wait-for-it.sh $DB_HOST:5432 --strict --timeout=30

python manage.py makemigrations
python manage.py migrate movies --fake
python manage.py migrate

if [ "$DEBUG" != 'True' ]; then 
    uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini
else
    python manage.py runserver 0.0.0.0:8000
fi