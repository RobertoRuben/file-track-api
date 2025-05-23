from datetime import datetime
from src.app.model.entity import DocumentCategory
from src.app.dto.request import DocumentCategoryRequestDTO
from src.app.dto.response import DocumentCategoryPage, DocumentCategoryResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IDocumentCategoryRepository
from src.app.service.interfaces import IDocumentCategoryService


class DocumentCategoryServiceImpl(IDocumentCategoryService):
    """
    Implementation of the document category service interface.

    Provides business logic for document category operations including creating,
    updating, deleting, and querying document categories.
    """

    def __init__(self, document_category_repository: IDocumentCategoryRepository):
        """
        Initialize the document category service with a repository.

        :param document_category_repository: The document category repository implementation
        """
        self.document_category_repository = document_category_repository

    @handle_exceptions
    async def add_document_category(
        self, document_category_request: DocumentCategoryRequestDTO
    ) -> DocumentCategoryResponseDTO:
        """
        Create a new document category.

        Validates that the category name does not already exist before creating the new entry.

        :param document_category_request: DTO containing the document category data
        :return: A DTO containing the created document category details
        :raises ConflictException: If a document category with the same name already exists
        """
        exists_document_category = await self.document_category_repository.exists_by(
            name=document_category_request.name
        )
        if exists_document_category:
            raise ConflictException(
                details=f"Document category with name '{document_category_request.name}' already exists.",
            )

        new_document_category = DocumentCategory(name=document_category_request.name)

        created_document_category = await self.document_category_repository.save(
            new_document_category
        )

        return DocumentCategoryResponseDTO(
            id=created_document_category.id,
            name=created_document_category.name,
            created_at=created_document_category.created_at,
            updated_at=created_document_category.updated_at,
        )

    @handle_exceptions
    async def get_all_document_categories(self) -> list[DocumentCategoryResponseDTO]:
        """
        Retrieve all document categories.

        :return: A list of DTOs containing all document categories
        """
        document_categories = await self.document_category_repository.get_all()
        return [
            DocumentCategoryResponseDTO(
                id=document_category.id,
                name=document_category.name,
                created_at=document_category.created_at,
                updated_at=document_category.updated_at,
            )
            for document_category in document_categories
        ]

    @handle_exceptions
    async def update_document_category(
        self,
        document_category_id: int,
        document_category_request: DocumentCategoryRequestDTO,
    ) -> DocumentCategoryResponseDTO:
        """
        Update an existing document category.

        Validates that the document category exists and that the new name is not already taken.

        :param document_category_id: ID of the document category to update
        :param document_category_request: DTO containing the updated data
        :return: A DTO containing the updated document category details
        :raises NotFoundException: If the document category with the given ID does not exist
        :raises ConflictException: If another document category with the new name already exists
        """
        exists_document_category_id = await self.document_category_repository.exists_by(
            id=document_category_id
        )
        if not exists_document_category_id:
            raise NotFoundException(
                details=f"Document category with ID {document_category_id} not found.",
            )
        document_category = await self.document_category_repository.get_by_id(
            document_category_id
        )

        if document_category.name != document_category_request.name:
            name_exists = await self.document_category_repository.exists_by(
                name=document_category_request.name
            )
            if name_exists:
                raise ConflictException(
                    details=f"Document category with name '{document_category_request.name}' already exists.",
                )

        document_category.name = document_category_request.name
        document_category.updated_at = datetime.now()

        updated_document_category = await self.document_category_repository.save(
            document_category
        )

        return DocumentCategoryResponseDTO(
            id=updated_document_category.id,
            name=updated_document_category.name,
            created_at=updated_document_category.created_at,
            updated_at=updated_document_category.updated_at,
        )

    @handle_exceptions
    async def delete_document_category(
        self, document_category_id: int
    ) -> MessageResponse:
        """
        Delete a document category by its ID.

        :param document_category_id: ID of the document category to delete
        :return: A message response indicating success or failure
        :raises NotFoundException: If the document category with the given ID does not exist
        """
        exists_document_category_id = await self.document_category_repository.exists_by(
            id=document_category_id
        )
        if not exists_document_category_id:
            raise NotFoundException(
                details=f"Document category with ID {document_category_id} not found.",
            )
        response = await self.document_category_repository.delete(document_category_id)
        if response is True:
            return MessageResponse(
                message="Document category deleted successfully.",
                success=True,
                details=f"Document category with ID {document_category_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete document category.",
                success=False,
                details=f"Document category with ID {document_category_id} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def get_document_category_by_id(
        self, document_category_id: int
    ) -> DocumentCategoryResponseDTO:
        """
        Retrieve a document category by its ID.

        :param document_category_id: ID of the document category to retrieve
        :return: A DTO containing the document category details
        :raises NotFoundException: If the document category with the given ID does not exist
        """
        exists_document_category_id = await self.document_category_repository.exists_by(
            id=document_category_id
        )
        if not exists_document_category_id:
            raise NotFoundException(
                details=f"Document category with ID {document_category_id} not found.",
            )
        document_category = await self.document_category_repository.get_by_id(
            document_category_id
        )
        return DocumentCategoryResponseDTO(
            id=document_category.id,
            name=document_category.name,
            created_at=document_category.created_at,
            updated_at=document_category.updated_at,
        )

    @handle_exceptions
    async def get_paginated_document_categories(
        self, page: int, size: int
    ) -> DocumentCategoryPage:
        """
        Retrieve a paginated list of document categories.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :return: A page object containing document categories and pagination metadata
        :raises BadRequestException: If page or size values are invalid
        """
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid size number",
                details="Size number must be greater than 0.",
            )

        page_result = await self.document_category_repository.get_pageable(page, size)
        document_categories_response = [
            DocumentCategoryResponseDTO(
                id=document_category.id,
                name=document_category.name,
                created_at=document_category.created_at,
                updated_at=document_category.updated_at,
            )
            for document_category in page_result.data
        ]
        return DocumentCategoryPage(
            data=document_categories_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(
        self, page: int, size: int, search_term: str
    ) -> DocumentCategoryPage:
        """
        Search for document categories with name filtering and pagination.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :param search_term: Term to search for in document category names
        :return: A page object containing the filtered document categories and pagination metadata
        :raises BadRequestException: If page or size values are invalid
        :raises NotFoundException: If no document categories match the search criteria
        """
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid size number",
                details="Size number must be greater than 0.",
            )

        search_dict = {"name": search_term}

        page_result = await self.document_category_repository.find(
            page, size, search_dict
        )

        if not page_result.data:
            raise NotFoundException(
                details=f"No document categories found with search term: {search_term}",
            )

        document_categories_response = [
            DocumentCategoryResponseDTO(
                id=document_category.id,
                name=document_category.name,
                created_at=document_category.created_at,
                updated_at=document_category.updated_at,
            )
            for document_category in page_result.data
        ]

        return DocumentCategoryPage(
            data=document_categories_response,
            meta=page_result.meta,
        )
