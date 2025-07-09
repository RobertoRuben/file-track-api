from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.core.db.dependencies import get_async_session
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.repository.implementations import DocumentaryTopicRepositoryImpl


async def get_documentary_topic_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IDocumentaryTopicRepository:
    """
    Dependency function to get the documentary topic repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of IDocumentaryTopicRepository bound to the provided session
    """
    return DocumentaryTopicRepositoryImpl(session=session)
