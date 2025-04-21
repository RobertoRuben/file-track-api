from abc import ABC, abstractmethod
from src.app.model.entity import Document
from src.app.schema import Page
from typing import Any


class IDocumentRepository(ABC):
    """
    Interface for the Document Repository.
    """

    @abstractmethod
    async def save(self, document: Document) -> Document:
        """
        Save a document.

        :param document: The document to save
        :return: The saved document with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Document]:
        """
        Get all documents.

        :return: A list of all documents
        """
        pass

    @abstractmethod
    async def delete(self, document_id: int) -> bool:
        """
        Delete a document by its ID.

        :param document_id: The ID of the document to delete
        :return: True if the document was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, document_id: int) -> Document:
        """
        Get a document by its ID.

        :param document_id: The ID of the document to retrieve
        :return: The document found
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Get a paginated list of documents.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object with documents and pagination information
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
        Search for documents based on search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary with search parameters
        :return: A Page object with documents that match the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a document exists based on the given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a document matching the criteria exists, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_registration_code(self, registration_code: str) -> Document:
        """
        Get a document by its registration code.

        :param registration_code: The registration code of the document to retrieve
        :return: The document found
        """
        pass

    @abstractmethod
    async def find_by_current_date(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Search for documents based on the current date.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary with search parameters
        :return: A Page object with documents that match the search criteria
        """
        pass

    @abstractmethod
    async def get_last_registration_code(self) -> str | None:
        """
        Get the last registration code used for documents.

        :return: The last registration code
        """
        pass

    @abstractmethod
    async def get_pageable_by_current_date(self, page: int, size: int) -> Page:
        """
        Get a paginated list of documents created on the current date.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object with documents created today
        """
        pass

    @abstractmethod
    async def get_document_information_by_id(
        self, document_id: int
    ) -> dict[str, Any] | None:
        """
        Get detailed information about a document by its ID.

        :param document_id: The ID of the document to retrieve
        :return: The document with detailed information
        """
        pass
