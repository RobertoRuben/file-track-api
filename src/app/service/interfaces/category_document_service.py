from abc import ABC, abstractmethod
from src.app.schema import MessageResponse
from src.app.dto.request import CategoryDocumentRequestDTO
from src.app.dto.response import CategoryDocumentResponseDTO, CategoryDocumentPage

class ICategoryDocumentService(ABC):
    """
    Interface for document category service operations.
    Defines the contract for document category-related business logic.
    """

    @abstractmethod
    async def add_category_document(self, category_document_request: CategoryDocumentRequestDTO) -> CategoryDocumentResponseDTO:
        """
        Add a new document category.

        Args:
            category_document_request: The data transfer object containing document category details.

        Returns:
            The created document category as a CategoryDocumentResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_categories_documents(self) -> list[CategoryDocumentResponseDTO]:
        """
        Retrieve all document categories.

        Returns:
            A list of CategoryDocumentResponseDTO objects representing all document categories.
        """
        pass

    @abstractmethod
    async def update_category_document(self, category_document_id: int, category_document_request: CategoryDocumentRequestDTO) -> CategoryDocumentResponseDTO:
        """
        Update an existing document category.

        Args:
            category_document_id: The ID of the document category to update.
            category_document_request: The data transfer object containing updated document category details.

        Returns:
            The updated document category as a CategoryDocumentResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_category_document(self, category_document_id: int) -> MessageResponse:
        """
        Delete a document category by its ID.

        Args:
            category_document_id: The ID of the document category to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_category_document_by_id(self, category_document_id: int) -> CategoryDocumentResponseDTO:
        """
        Retrieve a document category by its ID.

        Args:
            category_document_id: The ID of the document category to retrieve.

        Returns:
            The document category as a CategoryDocumentResponseDTO.
        """
        pass

    @abstractmethod
    async def get_paginated_category_documents(self, page: int, size: int) -> CategoryDocumentPage:
        """
        Retrieve a paginated list of document categories.

        Args:
            page: The page number to retrieve.
            size: The number of document categories per page.

        Returns:
            A CategoryDocumentPage object containing the paginated document categories.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> CategoryDocumentPage:
        """
        Find document categories based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of document categories per page.
            search_term: The term to search for in document category names.

        Returns:
            A CategoryDocumentPage object containing the document categories that match the search criteria.
        """
        pass