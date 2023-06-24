#!/usr/bin/env bash

python manage.py collectstatic
apt-get update
apt-get -y install gettext
python manage.py makemessages -l en -l ru
python manage.py compilemessages -l en -l ru

if [ "$DEBUG" != 'True' ]; then
    uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini
else
    python manage.py runserver service:8000
fi
# python manage.py runserver service:8000