FROM python:3.10

WORKDIR /opt/app

ENV DOCKER_CONTAINER=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

# COPY uwsgi/run_uwsgi.sh run_uwsgi.sh
COPY requirements.txt requirements.txt
# COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

# COPY . .

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "uwsgi/run_uwsgi.sh"]