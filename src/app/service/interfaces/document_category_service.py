from abc import ABC, abstractmethod
from src.app.schema import MessageResponse
from src.app.dto.request import DocumentCategoryRequestDTO
from src.app.dto.response import DocumentCategoryResponseDTO, DocumentCategoryPage


class IDocumentCategoryService(ABC):
    """
    Interface for document category service operations.
    Defines the contract for document category-related business logic.
    """

    @abstractmethod
    async def add_document_category(
        self, document_category_request: DocumentCategoryRequestDTO
    ) -> DocumentCategoryResponseDTO:
        """
        Add a new document category.

        :param document_category_request: The data transfer object containing document category details
        :return: The created document category as a DocumentCategoryResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_document_categories(self) -> list[DocumentCategoryResponseDTO]:
        """
        Retrieve all document categories.

        :return: A list of DocumentCategoryResponseDTO objects representing all document categories
        """
        pass

    @abstractmethod
    async def update_document_category(
        self,
        document_category_id: int,
        document_category_request: DocumentCategoryRequestDTO,
    ) -> DocumentCategoryResponseDTO:
        """
        Update an existing document category.

        :param document_category_id: The ID of the document category to update
        :param document_category_request: The data transfer object containing updated document category details
        :return: The updated document category as a DocumentCategoryResponseDTO
        """
        pass

    @abstractmethod
    async def delete_document_category(
        self, document_category_id: int
    ) -> MessageResponse:
        """
        Delete a document category by its ID.

        :param document_category_id: The ID of the document category to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_document_category_by_id(
        self, document_category_id: int
    ) -> DocumentCategoryResponseDTO:
        """
        Retrieve a document category by its ID.

        :param document_category_id: The ID of the document category to retrieve
        :return: The document category as a DocumentCategoryResponseDTO
        """
        pass

    @abstractmethod
    async def get_paginated_document_categories(
        self, page: int, size: int
    ) -> DocumentCategoryPage:
        """
        Retrieve a paginated list of document categories.

        :param page: The page number to retrieve
        :param size: The number of document categories per page
        :return: A DocumentCategoryPage object containing the paginated document categories
        """
        pass

    @abstractmethod
    async def find(
        self, page: int, size: int, search_term: str
    ) -> DocumentCategoryPage:
        """
        Find document categories based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of document categories per page
        :param search_term: The term to search for in document category names
        :return: A DocumentCategoryPage object containing the document categories that match the search criteria
        """
        pass
