from fastapi import Depends
from src.app.service.interfaces import ICategoryDocumentService
from src.app.service.implementations import CategoryDocumentServiceImpl
from src.app.repository.interfaces import ICategoriaDocumentoRepository
from src.app.repository.dependencies import get_categoria_documento_repository

async def get_category_document_service(repository: ICategoriaDocumentoRepository = Depends(get_categoria_documento_repository)) -> ICategoryDocumentService:
    """
    Dependency function to get the category document service implementation.

    This function creates and provides an instance of the category document service
    implementation with the necessary repository dependency injected.

    Args:
        repository: The category document repository implementation provided by
                   the FastAPI dependency injection system.

    Returns:
        An implementation of ICategoryDocumentService configured with the provided repository.
    """
    return CategoryDocumentServiceImpl(repository=repository)