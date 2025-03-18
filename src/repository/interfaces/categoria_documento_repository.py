from abc import ABC, abstractmethod
from src.model.entity import CategoriaDocumento
from src.schema import Page


class ICategoriaDocumentoRepository(ABC):
    """
    Interface for the CategoriaDocumento repository.
    """

    @abstractmethod
    async def save(self, categoria_documento: CategoriaDocumento) -> CategoriaDocumento:
        """
        Save a document category.

        Args:
            categoria_documento: The document category to save

        Returns:
            The saved document category with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[CategoriaDocumento]:
        """
        Get all document categories.

        Returns:
            A list containing all document categories
        """
        pass

    @abstractmethod
    async def delete(self, category_document_id: int) -> bool:
        """
        Delete a document category by its ID.

        Args:
            category_document_id: The ID of the document category to delete

        Returns:
            True if the category was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, category_document_id: int) -> CategoriaDocumento:
        """
        Get a document category by its ID.

        Args:
            category_document_id: The ID of the document category to retrieve

        Returns:
            The found document category
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Get a paginated list of document categories.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing document categories and pagination information
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

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with document categories matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a document category exists based on the given criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching document category exists, False otherwise
        """
        pass