from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.database import get_session_factory


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session_factory = get_session_factory()
    session = session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()
