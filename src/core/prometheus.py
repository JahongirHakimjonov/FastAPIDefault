import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from functools import cache

from fastapi import Request, Response
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

from core.settings import get_settings


@dataclass
class Metrics:
    request_count: Counter
    request_latency: Histogram


@cache
def get_metrics() -> Metrics:
    settings = get_settings()
    return Metrics(
        request_count=Counter(
            f"{settings.app_name}_request_count",
            "Total number of requests",
            ["method", "endpoint"],
        ),
        request_latency=Histogram(
            f"{settings.app_name}_request_latency_seconds",
            "Latency of requests in seconds",
            ["method", "endpoint"],
        ),
    )


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.time()
        response = await call_next(request)
        if not request.url.path.startswith("/api"):
            return response

        process_time = time.time() - start_time

        labels = {"method": request.method, "endpoint": request.url.path}
        metrics = get_metrics()
        metrics.request_count.labels(**labels).inc()
        metrics.request_latency.labels(**labels).observe(process_time)

        return response
