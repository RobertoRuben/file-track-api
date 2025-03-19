from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.dependencies import get_async_session
from src.repository.interfaces import IRolRepository
from src.repository.implementations import RolRepositoryImpl

async def get_rol_repository(session: AsyncSession = Depends(get_async_session)) -> IRolRepository:
    """
    Dependency function to get the role repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of IRolRepository bound to the provided session
    """
    return RolRepositoryImpl(session=session)