from fastapi import Depends
from src.service.interfaces import ICategoryDocumentService
from src.service.implementations import CategoryDocumentServiceImpl
from src.repository.interfaces import ICategoriaDocumentoRepository
from src.repository.dependencies import get_categoria_documento_repository

async def get_category_document_service(repository: ICategoriaDocumentoRepository = Depends(get_categoria_documento_repository)) -> ICategoryDocumentService:
    """
    Dependency injection for the CategoryDocumentService.
    """
    return CategoryDocumentServiceImpl(repository=repository)