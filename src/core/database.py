from functools import cache

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from core.settings import get_settings


@cache
def get_db_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(
        settings.postgres_url,
        echo=settings.postgres_echo,
        pool_size=20,
        pool_pre_ping=True,
        pool_use_lifo=True,
    )


@cache
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    engine = get_db_engine()
    return async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
