from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.core.db.dependencies import get_async_session
from src.app.domain.submitter.repository.interface import ISubmitterRepository
from src.app.domain.submitter.repository.implementations import SubmitterRepositoryImpl


async def get_submitter_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ISubmitterRepository:
    """
    Dependency function to get the submitter repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of ISubmitterRepository bound to the provided session
    """
    return SubmitterRepositoryImpl(session=session)
