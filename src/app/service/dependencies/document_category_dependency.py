from fastapi import Depends
from src.app.service.interfaces import IDocumentCategoryService
from src.app.service.implementations import DocumentCategoryServiceImpl
from src.app.repository.interfaces import IDocumentCategoryRepository
from src.app.repository.dependencies import get_document_category_repository


async def get_document_category_service(
    document_category_repository: IDocumentCategoryRepository = Depends(
        get_document_category_repository
    ),
) -> IDocumentCategoryService:
    """
    Dependency function to get the document category service implementation.

    This function creates and provides an instance of the document category service
    implementation with the necessary repository dependency injected.

    :param document_category_repository: The document category repository implementation
                                        provided by the FastAPI dependency injection system
    :return: An implementation of IDocumentCategoryService configured with the provided repository
    """
    return DocumentCategoryServiceImpl(
        document_category_repository=document_category_repository
    )
