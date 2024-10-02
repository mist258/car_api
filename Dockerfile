FROM python:3.11-alpine

MAINTAINER Backend dev

ENV PYTHONDONTWRITEBITYCODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CASHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.0.2 \
    POETRY_NOINTERACTION=1 \
    # DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

RUN apk update
RUN apk --no-cache add \
    gcc  \
    musl-dev \
    postgresql-dev \
    postgresql-client \
    curl

RUN mkdir /app
WORKDIR /app

ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH=$POETRY_HOME/bin:$PATH
COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-ansi
