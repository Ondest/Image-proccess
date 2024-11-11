FROM python:3.12-alpine

ARG POETRY_PARAMS=""
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.local/bin"

RUN apk update && apk add --no-cache \
    curl  \
    cargo \
    gcc  \
    libffi-dev \
    build-base \
    zlib-dev

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN mkdir /app
COPY pyproject.toml poetry.lock /app/
WORKDIR /app/
RUN poetry install -vv
COPY . .
