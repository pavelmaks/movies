FROM python:3.11
# set work directory
WORKDIR /opt/app/
ENV DOCKER_CONTAINER=1

COPY requirements.txt ./

RUN  pip install --upgrade pip \
    && pip install -r requirements.txt
# run app
ENTRYPOINT ["python", "main.py"]