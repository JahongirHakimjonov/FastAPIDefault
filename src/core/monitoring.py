import time
from importlib.metadata import version
from typing import Annotated

from fastapi import APIRouter, Header, Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest
from pydantic import BaseModel

from core.settings import get_settings

router = APIRouter()


class HealthcheckResponse(BaseModel):
    timestamp: int


class StatusResponse(BaseModel):
    app: str = "ok"


class VersionResponse(BaseModel):
    version: str


@router.get("/healthcheck", summary="Проверить доступность сервиса")
def ping() -> HealthcheckResponse:
    return HealthcheckResponse(timestamp=int(time.time()))


@router.get("/status", summary="Проверить статус используемых сервисов")
async def status() -> StatusResponse:
    return StatusResponse()


@router.get("/version", summary="Проверить версию приложения")
async def get_version() -> VersionResponse:
    settings = get_settings()
    return VersionResponse(version=version(settings.app_name))


@router.get("/metrics", summary="Получить метрики Prometheus")
async def metrics(key: Annotated[str, Header()] = "") -> Response:
    settings = get_settings()
    if key != settings.prometheus_metrics_key:
        return Response(status_code=403)
    data = generate_latest(REGISTRY)
    return Response(data, media_type=CONTENT_TYPE_LATEST)
