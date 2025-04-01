from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import IAreaConnectionRepository
from src.app.repository.implementations import AreaConnectionRepositoryImpl


async def get_area_connection_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IAreaConnectionRepository:
    """
    Dependency function to get the communication between areas repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of IComunicacionAreaRepository bound to the provided session
    """
    return AreaConnectionRepositoryImpl(session=session)
