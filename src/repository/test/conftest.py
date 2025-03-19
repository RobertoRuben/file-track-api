import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """
    Fixture that provides an event loop for the test session.
    This is required for running async tests with pytest.

    Returns:
        An asyncio event loop.
    """
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    """
    Creates an async SQLAlchemy engine connected to an in-memory SQLite database.
    The fixture initializes all database tables before tests and cleans up afterwards.

    Returns:
        An async SQLAlchemy engine instance.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def async_session_maker(async_engine):
    """
    Creates a factory for async database sessions.

    Args:
        async_engine: The async SQLAlchemy engine instance.

    Returns:
        A session factory that creates AsyncSession instances.
    """
    return sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest.fixture
async def async_session(async_session_maker):
    """
    Provides an async database session for tests.
    The session is automatically closed after each test.

    Args:
        async_session_maker: The async session factory.

    Returns:
        An AsyncSession instance.
    """
    async with async_session_maker() as session:
        yield session