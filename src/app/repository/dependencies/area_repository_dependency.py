from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import IAreaRepository
from src.app.repository.implementations import AreaRepositoryImpl

async def get_area_repository(session: AsyncSession = Depends(get_async_session)) -> IAreaRepository:
    """
    Dependency function to get the area repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of IAreaRepository bound to the provided session
    """
    return AreaRepositoryImpl(session=session)