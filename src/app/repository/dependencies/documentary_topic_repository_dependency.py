from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.repository.implementations import DocumentaryTopicRepositoryImpl

async def get_documentary_topic_repository(session: AsyncSession = Depends(AsyncSession)) -> IDocumentaryTopicRepository:
    """
    Dependency function to get the documentary topic repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of IDocumentaryTopicRepository bound to the provided session
    """
    return DocumentaryTopicRepositoryImpl(session=session)