from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api.router import api_router
from core.exceptions import register_exception_handlers
from core.lifespan import lifespan
from core.logger import configure_logger
from core.monitoring import router as monitoring_router
from core.prometheus import MetricsMiddleware
from core.sentry import init_sentry
from core.settings import get_settings


def create_app() -> FastAPI:
    """
    Create FastAPI application instance with middleware, routers, and exception handlers.
    """
    settings = get_settings()
    configure_logger()

    if settings.sentry_dsn:
        init_sentry()

    app = FastAPI(
        title=settings.app_title,
        root_path=settings.root_path,
        redoc_url=None,
        default_response_class=ORJSONResponse,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )

    app.add_middleware(MetricsMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=api_router, prefix="/api")
    app.include_router(router=monitoring_router, tags=["Monitoring"])

    register_exception_handlers(app)

    return app
