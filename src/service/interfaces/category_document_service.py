from abc import ABC, abstractmethod
from src.schema import MessageResponse
from src.dto.request import CategoryDocumentRequestDTO
from src.dto.response import CategoryDocumentResponseDTO, CategoryDocumentPage

class ICategoryDocumentService(ABC):
    @abstractmethod
    async def add_category_document(self, category_document_request: CategoryDocumentRequestDTO) -> CategoryDocumentResponseDTO:
        """Add a new category document."""
        pass

    @abstractmethod
    async def get_all_categories_documents(self) -> list[CategoryDocumentResponseDTO]:
        """Retrieve all category documents."""
        pass

    @abstractmethod
    async def update_category_document(self, category_document_id: int, category_document_request: CategoryDocumentRequestDTO) -> CategoryDocumentResponseDTO:
        """Update an existing category document."""
        pass

    @abstractmethod
    async def delete_category_document(self, category_document_id: int) -> MessageResponse:
        """Delete a category document by its ID."""
        pass

    @abstractmethod
    async def get_category_document_by_id(self, category_document_id: int) -> CategoryDocumentResponseDTO:
        """Retrieve a category document by its ID."""
        pass

    @abstractmethod
    async def get_paginated_category_documents(self, page: int, size: int) -> CategoryDocumentPage:
        """Retrieve paginated category documents."""
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> CategoryDocumentPage:
        """Find category documents with pagination."""
        pass
