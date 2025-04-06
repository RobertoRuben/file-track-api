from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import IDocumentCategoryRepository
from src.app.repository.implementations import DocumentCategoryRepositoryImpl


async def get_document_category_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IDocumentCategoryRepository:
    """
    Dependency function to get the document category repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of IDocumentCategoryRepository bound to the provided session
    """
    return DocumentCategoryRepositoryImpl(session=session)
