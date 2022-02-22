# syntax=docker/dockerfile:1
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./VERSION.txt /code/VERSION.txt
COPY ./setup.cfg /code/setup.cfg
COPY ./setup.py /code/setup.py

COPY ./src /code/src
COPY ./pipeline /code/pipeline
COPY ./secrets /code/secrets
COPY ./models /code/models

RUN pip install /code

ARG SERVICE_PATH
ENV SERVICE_PATH=${SERVICE_PATH}

CMD uvicorn ${SERVICE_PATH} --host 0.0.0.0 --port 8000
