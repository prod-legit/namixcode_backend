ARG WORK_DIR=/opt
ARG APP_USER=app

FROM python:3.12.4-slim AS prod
LABEL description="Namixcode backend image"

ARG WORK_DIR
ARG APP_USER

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VERSION=1.8.3

WORKDIR $WORK_DIR

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==$POETRY_VERSION \
    && poetry install --only=main --no-ansi --no-interaction

COPY . .

RUN \
    adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    $APP_USER \
    && chown $APP_USER:$APP_USER $WORK_DIR

USER $APP_USER

EXPOSE 8000

ENTRYPOINT ["python", "-m", "app"]

FROM prod AS dev
LABEL description="Namixcode backend image (dev)"

ARG WORK_DIR
ARG APP_USER
WORKDIR $WORK_DIR

USER root

RUN poetry install --no-ansi --no-interaction

USER $APP_USER
