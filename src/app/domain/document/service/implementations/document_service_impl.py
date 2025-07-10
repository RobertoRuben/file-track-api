import os
import mimetypes
from datetime import datetime
from src.app.core.helpers import document_helper
from src.app.core.exception.decorator import handle_exceptions
from src.app.core.security.auth.model import CurrentUser
from src.app.core.schema import MessageResponse
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.domain.document.model import Document
from src.app.domain.document.dto.request import DocumentRequestDTO
from src.app.domain.document.dto.response import (
    DocumentResponseDTO,
    DocumentPage,
)
from src.app.domain.document.repository.interface import (
    IDocumentRepository,
    IDocumentCategoryRepository,
    IDocumentaryTopicRepository,
)
from src.app.domain.submitter.repository.interface import ISubmitterRepository
from src.app.domain.location.repository.interface import IHamletRepository, ISettlementRepository
from src.app.domain.document.service.interface import IDocumentService, IReportService



class DocumentServiceImpl(IDocumentService):
    """
    Implementation of the Document Service interface.

    Provides business logic for document operations including creating, updating, deleting, and retrieving documents.
    """

    def __init__(
        self,
        document_repository: IDocumentRepository,
        document_category_repository: IDocumentCategoryRepository,
        submitter_repository: ISubmitterRepository,
        hamlet_repository: IHamletRepository,
        settlement_repository: ISettlementRepository,
        documentary_topic_repository: IDocumentaryTopicRepository,
        report_service: IReportService,
    ):
        """
        Initialize the DocumentService with repositories and services.

        :param document_repository: An instance of IDocumentRepository for database operations
        :param document_category_repository: Repository for document category operations
        :param submitter_repository: Repository for submitter operations
        :param hamlet_repository: Repository for hamlet operations
        :param settlement_repository: Repository for settlement operations
        :param documentary_topic_repository: Repository for documentary topic operations
        :param report_service: Service for generating reports
        """
        self.document_repository = document_repository
        self.document_category_repository = document_category_repository
        self.submitter_repository = submitter_repository
        self.hamlet_repository = hamlet_repository
        self.settlement_repository = settlement_repository
        self.documentary_topic_repository = documentary_topic_repository
        self.report_service = report_service

    @handle_exceptions
    async def add_document(
        self, document_request: DocumentRequestDTO, current_user: CurrentUser
    ) -> DocumentResponseDTO:
        """
        Add a new document to the system.

        :param document_request: The document request DTO containing document details
        :param current_user: Current user information including ID
        :return: A DTO containing the created document information
        :raises BadRequestException: If the document file is too large
        :raises NotFoundException: If any related entity doesn't exist
        :raises ConflictException: If a document with the same title already exists
        """
        MAX_FILE_SIZE_MB = 10
        MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

        if len(document_request.document) > MAX_FILE_SIZE_BYTES:
            raise BadRequestException(
                message="Document file too large",
                details=f"Document file size exceeds the maximum allowed size of {MAX_FILE_SIZE_MB}MB.",
            )

        exists_category = await self.document_category_repository.exists_by(
            id=document_request.document_category_id
        )

        if not exists_category:
            raise NotFoundException(
                message="Document category not found",
                details=f"Category with ID {document_request.document_category_id} not found.",
            )

        exists_documentary_topic = await self.documentary_topic_repository.exists_by(
            id=document_request.documentary_topic_id
        )

        if not exists_documentary_topic:
            raise NotFoundException(
                message="Documentary topic not found",
                details=f"Documentary topic with ID {document_request.documentary_topic_id} not found.",
            )

        exists_settlement = await self.settlement_repository.exists_by(
            id=document_request.settlement_id
        )

        if not exists_settlement:
            raise NotFoundException(
                message="Settlement not found",
                details=f"Settlement with ID {document_request.settlement_id} not found.",
            )

        if document_request.hamlet_id:
            exists_hamlet = await self.hamlet_repository.exists_by(
                id=document_request.hamlet_id
            )

            if not exists_hamlet:
                raise NotFoundException(
                    message="Hamlet not found",
                    details=f"Hamlet with ID {document_request.hamlet_id} not found.",
                )

        exists_submitter = await self.submitter_repository.exists_by(
            id=document_request.submitter_id
        )

        if not exists_submitter:
            raise NotFoundException(
                message="Submitter not found",
                details=f"Submitter with ID {document_request.submitter_id} not found.",
            )

        exists_doc_with_title = await self.document_repository.exists_by(
            title=document_request.title
        )

        if exists_doc_with_title:
            raise ConflictException(
                message="Document title already exists",
                details=f"Document with title '{document_request.title}' already exists.",
            )

        storage_path, file_size = await document_helper.save_document_file(
            document_request.document
        )

        last_registration_code = (
            await self.document_repository.get_last_registration_code()
        )

        registration_code = document_helper.generate_registration_code(
            last_registration_code
        )

        new_document = Document(
            registration_code=registration_code,
            title=document_request.title,
            subject=document_request.subject,
            pages=document_request.pages,
            storage_path=storage_path,
            size=file_size,
            submitter_id=document_request.submitter_id,
            document_category_id=document_request.document_category_id,
            documentary_topic_id=document_request.documentary_topic_id,
            hamlet_id=document_request.hamlet_id,
            settlement_id=document_request.settlement_id,
            registered_by_user_id=current_user.id,
        )

        created_document = await self.document_repository.save(new_document)

        return DocumentResponseDTO(
            id=created_document.id,
            registration_code=created_document.registration_code,
            title=created_document.title,
            subject=created_document.subject,
            pages=created_document.pages,
            storage_path=created_document.storage_path,
            size=created_document.size,
            submitter_id=created_document.submitter_id,
            document_category_id=created_document.document_category_id,
            documentary_topic_id=created_document.documentary_topic_id,
            hamlet_id=created_document.hamlet_id,
            settlement_id=created_document.settlement_id,
            registered_by_user_id=created_document.registered_by_user_id,
            created_at=created_document.created_at,
            updated_at=created_document.updated_at,
        )

    @handle_exceptions
    async def get_all_documents(self) -> list[DocumentResponseDTO]:
        """
        Retrieve all documents from the repository.

        :return: A list of document response DTOs
        """
        documents = await self.document_repository.get_all()
        return [
            DocumentResponseDTO(
                id=doc.id,
                registration_code=doc.registration_code,
                title=doc.title,
                subject=doc.subject,
                pages=doc.pages,
                storage_path=doc.storage_path,
                size=doc.size,
                submitter_id=doc.submitter_id,
                document_category_id=doc.document_category_id,
                documentary_topic_id=doc.documentary_topic_id,
                hamlet_id=doc.hamlet_id,
                settlement_id=doc.settlement_id,
                registered_by_user_id=doc.registered_by_user_id,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
            )
            for doc in documents
        ]

    @handle_exceptions
    async def update_document(
        self, document_id: int, document_request: DocumentRequestDTO, user_id: int
    ) -> DocumentResponseDTO:
        """
        Update an existing document in the system.

        :param document_id: ID of the document to update
        :param document_request: The request DTO containing the new document details
        :param user_id: ID of the user who is updating the document
        :return: A DTO containing the updated document information
        :raises BadRequestException: If the document file is too large
        :raises NotFoundException: If the document or any related entity doesn't exist
        :raises ConflictException: If a document with the same title already exists
        """
        existing_document = await self.document_repository.get_by_id(document_id)

        if not existing_document:
            raise NotFoundException(
                message="Document not found",
                details=f"Document with ID {document_id} not found.",
            )

        exists_category = await self.document_category_repository.exists_by(
            id=document_request.document_category_id
        )

        if not exists_category:
            raise NotFoundException(
                message="Document category not found",
                details=f"Category with ID {document_request.document_category_id} not found.",
            )

        exists_documentary_topic = await self.documentary_topic_repository.exists_by(
            id=document_request.documentary_topic_id
        )

        if not exists_documentary_topic:
            raise NotFoundException(
                message="Documentary topic not found",
                details=f"Documentary topic with ID {document_request.documentary_topic_id} not found.",
            )

        exists_settlement = await self.settlement_repository.exists_by(
            id=document_request.settlement_id
        )

        if not exists_settlement:
            raise NotFoundException(
                message="Settlement not found",
                details=f"Settlement with ID {document_request.settlement_id} not found.",
            )

        if document_request.hamlet_id:
            exists_hamlet = await self.hamlet_repository.exists_by(
                id=document_request.hamlet_id
            )

            if not exists_hamlet:
                raise NotFoundException(
                    message="Hamlet not found",
                    details=f"Hamlet with ID {document_request.hamlet_id} not found.",
                )

        exists_submitter = await self.submitter_repository.exists_by(
            id=document_request.submitter_id
        )

        if not exists_submitter:
            raise NotFoundException(
                message="Submitter not found",
                details=f"Submitter with ID {document_request.submitter_id} not found.",
            )

        if document_request.title != existing_document.title:
            exists_doc_with_title = await self.document_repository.exists_by(
                title=document_request.title
            )

            if exists_doc_with_title:
                raise ConflictException(
                    message="Document title already exists",
                    details=f"A document with title '{document_request.title}' already exists.",
                )

        storage_path = existing_document.storage_path
        file_size = existing_document.size

        if document_request.document and document_request.document != b'':
            MAX_FILE_SIZE_MB = 10
            MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

            if len(document_request.document) > MAX_FILE_SIZE_BYTES:
                raise BadRequestException(
                    message="Document file too large",
                    details=f"Document file size exceeds the maximum allowed size of {MAX_FILE_SIZE_MB}MB.",
                )

            storage_path, file_size = await document_helper.save_document_file(
                document_request.document
            )

        existing_document.title = document_request.title
        existing_document.subject = document_request.subject
        existing_document.pages = document_request.pages
        existing_document.storage_path = storage_path
        existing_document.size = file_size
        existing_document.submitter_id = document_request.submitter_id
        existing_document.document_category_id = document_request.document_category_id
        existing_document.documentary_topic_id = document_request.documentary_topic_id
        existing_document.hamlet_id = document_request.hamlet_id
        existing_document.settlement_id = document_request.settlement_id
        existing_document.updated_at = datetime.now()

        updated_document = await self.document_repository.save(existing_document)

        return DocumentResponseDTO(
            id=updated_document.id,
            registration_code=updated_document.registration_code,
            title=updated_document.title,
            subject=updated_document.subject,
            pages=updated_document.pages,
            storage_path=updated_document.storage_path,
            size=updated_document.size,
            submitter_id=updated_document.submitter_id,
            document_category_id=updated_document.document_category_id,
            documentary_topic_id=updated_document.documentary_topic_id,
            hamlet_id=updated_document.hamlet_id,
            settlement_id=updated_document.settlement_id,
            registered_by_user_id=updated_document.registered_by_user_id,
            created_at=updated_document.created_at,
            updated_at=updated_document.updated_at,
        )

    @handle_exceptions
    async def delete_document(self, document_id: int) -> MessageResponse:
        """
        Delete a document from the system.

        :param document_id: ID of the document to delete
        :return: A DTO containing information about the deleted document
        :raises NotFoundException: If the document doesn't exist
        """
        existing_document = await self.document_repository.get_by_id(document_id)

        if not existing_document:
            raise NotFoundException(
                message="Document not found",
                details=f"Document with ID {document_id} not found.",
            )

        response = await self.document_repository.delete(document_id)

        if response is True:
            return MessageResponse(
                message="Document deleted successfully",
                success=True,
                details=f"Document with code {existing_document.registration_code} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Document deletion failed",
                success=False,
                details=f"Document with code {existing_document.registration_code} deletion failed.",
                status_code=500,
            )

    @handle_exceptions
    async def get_document_by_id(self, document_id: int) -> DocumentResponseDTO:
        """
        Retrieve a document by its ID.

        :param document_id: ID of the document to retrieve
        :return: A DTO containing the document information
        :raises NotFoundException: If the document doesn't exist
        """
        document = await self.document_repository.get_by_id(document_id)

        if not document:
            raise NotFoundException(
                message="Document not found",
                details=f"Document with ID {document_id} not found.",
            )

        return DocumentResponseDTO(
            id=document.id,
            registration_code=document.registration_code,
            title=document.title,
            subject=document.subject,
            pages=document.pages,
            storage_path=document.storage_path,
            size=document.size,
            submitter_id=document.submitter_id,
            document_category_id=document.document_category_id,
            documentary_topic_id=document.documentary_topic_id,
            hamlet_id=document.hamlet_id,
            settlement_id=document.settlement_id,
            registered_by_user_id=document.registered_by_user_id,
            created_at=document.created_at,
            updated_at=document.updated_at,
        )

    @handle_exceptions
    async def get_documents_paginated(self, page: int, size: int) -> DocumentPage:
        """
        Retrieve documents in a paginated format.

        :param page: The page number to retrieve (starts at 1)
        :param size: The number of documents per page
        :return: A DocumentPage object containing the paginated documents
        :raises BadRequestException: If the pagination parameters are invalid
        :raises NotFoundException: If there are no documents on the specified page
        """
        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        page_result = await self.document_repository.get_pageable(page, size)

        if not page_result.data:
            raise NotFoundException(
                message="No documents found",
                details=f"No documents found on page {page}.",
            )

        document_responses = [
            DocumentResponseDTO(**document_dict) for document_dict in page_result.data
        ]

        return DocumentPage(
            data=document_responses,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search: str) -> DocumentPage:
        """
        Search for documents based on a search string.

        :param page: The page number to retrieve (starts at 1)
        :param size: The number of documents per page
        :param search: The search query string
        :return: A DocumentPage object containing the search results
        :raises BadRequestException: If the pagination parameters are invalid
        :raises NotFoundException: If no documents match the search
        """
        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        search_dict = {
            "registration_code": search,
            "title": search,
            "subject": search,
            "submitter_dni": search,
        }

        page_result = await self.document_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                message="No documents found",
                details=f"No documents found matching the search '{search}'.",
            )

        document_responses = [
            DocumentResponseDTO(**document_dict) for document_dict in page_result.data
        ]

        return DocumentPage(
            data=document_responses,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def get_document_by_registration_code(
        self, registration_code: str
    ) -> tuple[bytes, str, str]:
        """
        Retrieve a document file by its registration code.

        :param registration_code: The registration code of the document to retrieve
        :return: A tuple containing the document content, filename, and content type
        :raises NotFoundException: If the document doesn't exist
        """
        document = await self.document_repository.get_by_registration_code(
            registration_code
        )

        if not document:
            raise NotFoundException(
                message="Document not found",
                details=f"Document with registration code '{registration_code}' not found.",
            )

        if not os.path.exists(document.storage_path):
            raise NotFoundException(
                message="Document file not found",
                details=f"Document file for code '{registration_code}' not found in storage.",
            )

        with open(document.storage_path, "rb") as file:
            content = file.read()

        filename = f"{document.title.lower().replace(' ', '_')}_{registration_code}.pdf"

        content_type, _ = mimetypes.guess_type(document.storage_path)
        if not content_type:
            content_type = "application/pdf"

        return content, filename, content_type

    @handle_exceptions
    async def get_documents_by_current_date(self, page: int, size: int) -> DocumentPage:
        """
        Retrieve documents created on the current date in a paginated format.

        This method fetches all documents that were created today and returns them
        with pagination to manage large datasets efficiently.

        :param page: The page number to retrieve (starts at 1)
        :param size: The number of documents per page
        :return: A DocumentPage object containing the documents created today
        :raises BadRequestException: If the pagination parameters are invalid
        :raises NotFoundException: If no documents are found for the current date
        """
        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        page_result = await self.document_repository.get_pageable_by_current_date(
            page, size
        )

        if not page_result.data:
            raise NotFoundException(
                message="No documents found",
                details=f"No documents found on page {page}.",
            )

        document_responses = [
            DocumentResponseDTO(**document_dict) for document_dict in page_result.data
        ]

        return DocumentPage(
            data=document_responses,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find_by_current_date(
        self, page: int, size: int, search: str
    ) -> DocumentPage:
        """
        Search for documents created on the current date based on a search string.

        This method searches for documents created today that match the provided search
        criteria. The search is performed on registration code, title, subject,
        and submitter DNI fields. Results are returned with pagination.

        :param page: The page number to retrieve (starts at 1)
        :param size: The number of documents per page
        :param search: The search term to match against document fields
        :return: A DocumentPage object containing the documents that match the search criteria
        :raises BadRequestException: If the pagination parameters are invalid
        :raises NotFoundException: If no documents match the search criteria for today
        """

        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        search_dict = {
            "registration_code": search,
            "title": search,
            "subject": search,
            "submitter_dni": search,
        }

        page_result = await self.document_repository.find_by_current_date(
            page, size, search_dict
        )

        if not page_result.data:
            raise NotFoundException(
                message="No documents found",
                details=f"No documents found matching the search '{search}'.",
            )

        document_responses = [
            DocumentResponseDTO(**document_dict) for document_dict in page_result.data
        ]

        return DocumentPage(
            data=document_responses,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def get_document_information_by_id(
        self, document_id: int
    ) -> DocumentResponseDTO:
        """
        Retrieve detailed information about a document by its ID.

        This method fetches a document with additional details such as related
        topics, categories, settlements, and submitter information.

        :param document_id: The ID of the document to retrieve
        :return: A DTO containing the detailed document information
        :raises NotFoundException: If the document doesn't exist
        """
        document_info = await self.document_repository.get_document_information_by_id(
            document_id
        )

        if not document_info:
            raise NotFoundException(
                message="Document not found",
                details=f"Document with ID {document_id} not found.",
            )

        return DocumentResponseDTO(
            id=document_info["id"],
            registration_code=document_info["registration_code"],
            title=document_info["title"],
            subject=document_info["subject"],
            pages=document_info["pages"],
            submitter_dni=document_info.get("submitter_dni"),
            submitter_names=document_info.get("submitter_names"),
            document_category_name=document_info.get("document_category_name"),
            documentary_topic_name=document_info.get("documentary_topic_name"),
            settlement_name=document_info.get("settlement_name"),
            hamlet_name=document_info.get("hamlet_name"),
            registered_by_user_name=document_info.get("registered_by_username"),
            created_at=document_info["created_at"],
        )

    @handle_exceptions
    async def generate_document_registration_report(
        self, document_id: int
    ) -> tuple[bytes, str]:
        """
        Generates a document registration report in PDF format.

        :param document_id: The ID of the document to generate the report for
        :return: A tuple containing the PDF content and the filename
        :raises NotFoundException: If the document does not exist
        """
        document_info = await self.get_document_information_by_id(document_id)

        if not document_info:
            raise NotFoundException(
                message="Document not found",
                details=f"Document with ID {document_id} not found.",
            )

        pdf_content = await self.report_service.generate_document_registration_report(
            document_info
        )

        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{document_info.registration_code}_{current_datetime}.pdf"

        return pdf_content, filename
