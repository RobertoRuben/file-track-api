from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db.database import engine


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create and yield an asynchronous database session.

    This dependency function creates and yields an AsyncSession instance
    for interacting with the database asynchronously. The session is automatically
    created at the beginning of a request and closed when the request is complete.

    The session is configured with:
    - expire_on_commit=False: To prevent SQLAlchemy from expiring objects after commit
    - autocommit=False: To maintain explicit transaction control
    - autoflush=False: To require explicit flushing of changes

    Yields:
        AsyncSession: An async SQLAlchemy session for database operations
    """
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()