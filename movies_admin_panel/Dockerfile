FROM python:3.10

WORKDIR /opt/app

ENV DOCKER_CONTAINER=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY app/uwsgi/run_uwsgi.sh uwsgi/run_uwsgi.sh
COPY requirements.txt requirements.txt
COPY app/uwsgi/wait-for-it.sh uwsgi/wait-for-it.sh

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

RUN ["chmod", "+x", "./uwsgi/wait-for-it.sh"]

COPY app .

EXPOSE 8000

CMD ["/bin/sh", "uwsgi/run_uwsgi.sh"]