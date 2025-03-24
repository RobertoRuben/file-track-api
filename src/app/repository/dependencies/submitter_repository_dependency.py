from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import ISubmitterRepository
from src.app.repository.implementations import SubmitterRepositoryImpl


async def get_submitter_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ISubmitterRepository:
    """
    Dependency function to get the remitente (sender) repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of IRemitenteRepository bound to the provided session
    """
    return SubmitterRepositoryImpl(session=session)
