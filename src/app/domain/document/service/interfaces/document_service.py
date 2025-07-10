from abc import ABC, abstractmethod
from src.app.domain.document.dto import DocumentRequestDTO
from src.app.domain.document.dto import (
    DocumentResponseDTO,
    DocumentPage,
    CurrentUserResponseDTO,
)
from src.app.core.schema import MessageResponse


class IDocumentService(ABC):
    """
    Abstract base class for Document Service.

    This class defines the interface for document-related operations.
    """

    @abstractmethod
    async def add_document(
        self, document_request: DocumentRequestDTO, current_user: CurrentUserResponseDTO
    ) -> DocumentResponseDTO:
        """
        Add a new document.

        :param document_request: The data transfer object containing document details
        :param current_user: The current user making the request
        :return: The created document as a DocumentResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_documents(self) -> list[DocumentResponseDTO]:
        """
        Retrieve all documents.

        :return: A list of DocumentResponseDTO objects representing all documents
        """
        pass

    @abstractmethod
    async def update_document(
        self, document_id: int, document_request: DocumentRequestDTO
    ) -> DocumentResponseDTO:
        """
        Update an existing document.

        :param document_id: The ID of the document to update
        :param document_request: The data transfer object containing updated document details
        :return: The updated document as a DocumentResponseDTO
        """
        pass

    @abstractmethod
    async def delete_document(self, document_id: int) -> MessageResponse:
        """
        Delete a document by its ID.

        :param document_id: The ID of the document to delete
        :return: A DocumentResponseDTO indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_document_by_id(self, document_id: int) -> DocumentResponseDTO:
        """
        Retrieve a document by its ID.

        :param document_id: The ID of the document to retrieve
        :return: The document as a DocumentResponseDTO
        """
        pass

    @abstractmethod
    async def get_documents_paginated(self, page: int, size: int) -> DocumentPage:
        """
        Retrieve documents in a paginated format.

        :param page: The page number to retrieve
        :param size: The number of documents per page
        :return: A DocumentPage containing the paginated documents
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search: str) -> DocumentPage:
        """
        Search for documents based on a query string.

        :param page: The page number to retrieve
        :param size: The number of documents per page
        :param search: The search query string
        :return: A DocumentPage containing the search results
        """
        pass

    @abstractmethod
    async def get_document_by_registration_code(
        self, registration_code: str
    ) -> tuple[bytes, str, str]:
        """
        Retrieve a document file by its registration code.

        :param registration_code: The registration code of the document to retrieve
        :return: A tuple containing the document content, filename, and content type
        :raises NotFoundException: If the document doesn't exist
        """
        pass

    @abstractmethod
    async def get_documents_by_current_date(self, page: int, size: int) -> DocumentPage:
        """
        Retrieve documents created on the current date in a paginated format.

        :param page: The page number to retrieve
        :param size: The number of documents per page
        :return: A DocumentPage containing the documents created on the current date
        :raises BadRequestException: If the pagination parameters are invalid
        :raises NotFoundException: If no documents are found for the current date
        """
        pass

    @abstractmethod
    async def find_by_current_date(
        self, page: int, size: int, search: str
    ) -> DocumentPage:
        """
        Search for documents created on the current date based on a query string.

        :param page: The page number to retrieve
        :param size: The number of documents per page
        :param search: The search query string
        :return: A DocumentPage containing the search results from documents created today
        :raises BadRequestException: If the pagination parameters are invalid
        :raises NotFoundException: If no documents match the search criteria for today
        """
        pass

    @abstractmethod
    async def get_document_information_by_id(
        self, document_id: int
    ) -> DocumentResponseDTO:
        """
        Retrieve detailed information about a document by its ID.

        :param document_id: The ID of the document to retrieve
        :return: The document with detailed information
        """
        pass

    @abstractmethod
    async def generate_document_registration_report(
        self, document_id: int
    ) -> tuple[bytes, str]:
        """
        Genera un reporte de registro de documento en formato PDF.

        :param document_id: El ID del documento para generar el reporte
        :return: Una tupla con el contenido del PDF y el nombre del archivo
        :raises NotFoundException: Si el documento no existe
        """
        pass
