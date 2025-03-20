"""
Database connection configuration and initialization module.

This module sets up the SQLAlchemy async engine for database connections
and provides functionality to initialize the database schema.
"""

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from src.app.config import settings
from src.app.model.entity import *

# Database connection URL from application settings
postgres_url = settings.database_url

# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(
    postgres_url,
    echo=settings.DB_ECHO_LOG,
    future=True,
    pool_size=5,  # Number of connections to keep open
    max_overflow=10,  # Maximum number of additional connections
    pool_timeout=30,  # Seconds to wait before timing out on getting a connection
    pool_pre_ping=True,  # Verify connections are alive before using them
    poolclass=AsyncAdaptedQueuePool  # Connection pool implementation
)


async def init_db():
    """
    Initialize the database schema.

    Creates all tables defined in SQLModel metadata if they don't exist.
    This function should be called during application startup to ensure
    the database structure is properly configured.

    The function uses a transaction to ensure schema creation is atomic.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)