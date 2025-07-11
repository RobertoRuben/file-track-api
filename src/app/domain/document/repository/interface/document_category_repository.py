from abc import ABC, abstractmethod

from src.app.core.schema import Page
from src.app.domain.document.model import DocumentCategory


class IDocumentCategoryRepository(ABC):
    """
    Interface for the DocumentCategory repository.
    Provides definitions for CRUD operations and search functionality.
    """

    @abstractmethod
    async def save(self, document_category: DocumentCategory) -> DocumentCategory:
        """
        Save a document category.

        :param document_category: The document category to save
        :return: The saved document category with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[DocumentCategory]:
        """
        Get all document categories.

        :return: A list containing all document categories
        """
        pass

    @abstractmethod
    async def delete(self, category_document_id: int) -> bool:
        """
        Delete a document category by its ID.

        :param category_document_id: The ID of the document category to delete
        :return: True if the category was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, category_document_id: int) -> DocumentCategory:
        """
        Get a document category by its ID.

        :param category_document_id: The ID of the document category to retrieve
        :return: The found document category or None if not found
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Get a paginated list of document categories.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing document categories and pagination information
        """
        pass

    @abstractmethod
    async def find(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Find document categories by search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with document categories matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a document category exists based on the given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching document category exists, False otherwise
        """
        pass

    @abstractmethod
    async def delete_by_ids(self, category_ids: list[int]) -> bool:
        """
        Delete multiple document category entities from the database by their IDs.

        :param category_ids: List of document category IDs to delete
        :return: True if the document categories were successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def find_by_ids(self, category_ids: list[int]) -> list[DocumentCategory]:
        """
        Find multiple document categories by their IDs.

        :param category_ids: List of document category IDs to find
        :return: List of DocumentCategory entities matching the provided IDs
        """
        pass
