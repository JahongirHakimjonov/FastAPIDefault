# syntax=docker/dockerfile:1.2
ARG PYTHON_VERSION=3.11
ARG UV_VERSION=0.7.2

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM python:${PYTHON_VERSION} AS builder
COPY --from=uv /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONBUFFERED=1

WORKDIR /app

# install dependencies with uv
RUN uv venv /app/.venv
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --no-dev --frozen --no-install-project --group docker

FROM python:${PYTHON_VERSION}-slim AS app

WORKDIR /app

ENV PYTHONBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:/app/src PATH=/app/.venv/bin:$PATH

COPY --from=builder /app/.venv .venv
COPY ./pyproject.toml ./uv.lock ./alembic.ini ./
COPY ./src /app/src

RUN chgrp -R 0 /app && chmod -R g=u /app

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "alembic upgrade head && uvicorn app:create_app --proxy-headers --workers=2 --loop uvloop --http httptools --host 0.0.0.0 --port 8000"]
