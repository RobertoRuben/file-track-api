from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.core.db.dependencies import get_async_session
from src.app.repository.interfaces import IDocumentRepository
from src.app.repository.implementations import DocumentRepositoryImpl


async def get_document_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IDocumentRepository:
    """
    Dependency function to get the document repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of IDocumentRepository bound to the provided session
    """
    return DocumentRepositoryImpl(session=session)
