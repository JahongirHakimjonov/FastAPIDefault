from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.database import get_db_engine
from core.requests import get_http_transport


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    db_engine = get_db_engine()
    http_transport = get_http_transport()
    yield
    await db_engine.dispose()
    await http_transport.aclose()
