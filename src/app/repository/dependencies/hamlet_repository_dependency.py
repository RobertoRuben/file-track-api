from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.core.db.dependencies import get_async_session
from src.app.repository.interfaces import IHamletRepository
from src.app.repository.implementations import HamletRepositoryImpl


async def get_hamlet_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IHamletRepository:
    """
    Dependency function to get the hamlet repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of IHamletRepository bound to the provided session
    """
    return HamletRepositoryImpl(session=session)
