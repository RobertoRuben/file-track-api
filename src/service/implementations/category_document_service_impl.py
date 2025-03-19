from datetime import datetime
from src.model.entity import CategoriaDocumento
from src.dto.request import CategoryDocumentRequestDTO
from src.dto.response import CategoryDocumentPage, CategoryDocumentResponseDTO
from src.schema import MessageResponse
from src.exception import BadRequestException, ConflictException, NotFoundException
from src.exception.decorator import handle_exceptions
from src.repository.interfaces import ICategoriaDocumentoRepository
from src.service.interfaces import ICategoryDocumentService


class CategoryDocumentServiceImpl(ICategoryDocumentService):
    """
    Implementation of the document category service interface.

    Provides business logic for document category operations including creating,
    updating, deleting, and querying document categories.
    """

    def __init__(self, repository: ICategoriaDocumentoRepository):
        """
        Initialize the document category service with a repository.

        Args:
            repository: The document category repository implementation
        """
        self.repository = repository

    @handle_exceptions
    async def add_category_document(
        self,
        category_document_request: CategoryDocumentRequestDTO
    ) -> CategoryDocumentResponseDTO:
        """
        Create a new document category.

        Validates that the category name does not already exist before creating the new entry.

        Args:
            category_document_request: DTO containing the document category data

        Returns:
            A DTO containing the created document category details

        Raises:
            ConflictException: If a document category with the same name already exists
        """
        exists_category_document = await self.repository.exists_by(nombre=category_document_request.nombre)
        if exists_category_document:
            raise ConflictException(
                details=f"Category document with name {category_document_request.nombre} already exists.",
            )

        new_category_document = CategoriaDocumento(
            nombre=category_document_request.nombre
        )

        created_category_document = await self.repository.save(new_category_document)

        return CategoryDocumentResponseDTO(
            id=created_category_document.id,
            nombre=created_category_document.nombre,
            created_at=created_category_document.created_at,
            updated_at=created_category_document.updated_at
        )

    @handle_exceptions
    async def get_all_categories_documents(self) -> list[CategoryDocumentResponseDTO]:
        """
        Retrieve all document categories.

        Returns:
            A list of DTOs containing all document categories
        """
        category_documents = await self.repository.get_all()
        return [
            CategoryDocumentResponseDTO(
                id=category_document.id,
                nombre=category_document.nombre,
                created_at=category_document.created_at,
                updated_at=category_document.updated_at
            )
            for category_document in category_documents
        ]

    @handle_exceptions
    async def update_category_document(
        self,
        category_document_id: int,
        category_document_request: CategoryDocumentRequestDTO
    ) -> CategoryDocumentResponseDTO:
        """
        Update an existing document category.

        Validates that the document category exists and that the new name is not already taken.

        Args:
            category_document_id: ID of the document category to update
            category_document_request: DTO containing the updated data

        Returns:
            A DTO containing the updated document category details

        Raises:
            NotFoundException: If the document category with the given ID does not exist
            ConflictException: If another document category with the new name already exists
        """
        exists_category_document_id = await self.repository.exists_by(id=category_document_id)
        if not exists_category_document_id:
            raise NotFoundException(
                details=f"Category document with ID {category_document_id} not found.",
            )
        category_document = await self.repository.get_by_id(category_document_id)

        if category_document.nombre != category_document_request.nombre:
            name_exists = await self.repository.exists_by(nombre=category_document_request.nombre)
            if name_exists:
                raise ConflictException(
                    details=f"Category document with name {category_document_request.nombre} already exists.",
                )

        category_document.nombre = category_document_request.nombre
        category_document.updated_at = datetime.now()

        updated_category_document = await self.repository.save(category_document)

        return CategoryDocumentResponseDTO(
            id=updated_category_document.id,
            nombre=updated_category_document.nombre,
            created_at=updated_category_document.created_at,
            updated_at=updated_category_document.updated_at
        )

    @handle_exceptions
    async def delete_category_document(self, category_document_id: int) -> MessageResponse:
        """
        Delete a document category by its ID.

        Args:
            category_document_id: ID of the document category to delete

        Returns:
            A message response indicating success or failure

        Raises:
            NotFoundException: If the document category with the given ID does not exist
        """
        exists_category_document_id = await self.repository.exists_by(id=category_document_id)
        if not exists_category_document_id:
            raise NotFoundException(
                details=f"Category document with ID {category_document_id} not found.",
            )
        response = await self.repository.delete(category_document_id)
        if response is True:
            return MessageResponse(
                message="Category document deleted successfully.",
                success=True,
                details=f"Category document with ID {category_document_id} deleted successfully.",
                status_code=200
            )
        else:
            return MessageResponse(
                message="Failed to delete category document.",
                success=False,
                details=f"Category document with ID {category_document_id} could not be deleted.",
                status_code=500
            )

    @handle_exceptions
    async def get_category_document_by_id(self, category_document_id: int) -> CategoryDocumentResponseDTO:
        """
        Retrieve a document category by its ID.

        Args:
            category_document_id: ID of the document category to retrieve

        Returns:
            A DTO containing the document category details

        Raises:
            NotFoundException: If the document category with the given ID does not exist
        """
        exists_category_document_id = await self.repository.exists_by(id=category_document_id)
        if not exists_category_document_id:
            raise NotFoundException(
                details=f"Category document with ID {category_document_id} not found.",
            )
        category_document = await self.repository.get_by_id(category_document_id)
        return CategoryDocumentResponseDTO(
            id=category_document.id,
            nombre=category_document.nombre,
            created_at=category_document.created_at,
            updated_at=category_document.updated_at
        )

    @handle_exceptions
    async def get_paginated_category_documents(self, page: int, size: int) -> CategoryDocumentPage:
        """
        Retrieve a paginated list of document categories.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page

        Returns:
            A page object containing document categories and pagination metadata

        Raises:
            BadRequestException: If page or size values are invalid
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

        page_result = await self.repository.get_pageable(page, size)
        category_documents_response = [
            CategoryDocumentResponseDTO(**category_document.__dict__) for category_document in page_result.data
        ]
        return CategoryDocumentPage(
            data=category_documents_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> CategoryDocumentPage:
        """
        Search for document categories with name filtering and pagination.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page
            search_term: Term to search for in document category names

        Returns:
            A page object containing the filtered document categories and pagination metadata

        Raises:
            BadRequestException: If page or size values are invalid
            NotFoundException: If no document categories match the search criteria
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

        search_dict = {
            "nombre": search_term
        }

        page_result = await self.repository.find(page, size, search_dict)

        if page_result.data is None:
            raise NotFoundException(
                details=f"No category document found with search term: {search_term}",
            )

        category_documents_response = [
            CategoryDocumentResponseDTO(**category_document.__dict__) for category_document in page_result.data
        ]

        return CategoryDocumentPage(
            data=category_documents_response,
            meta=page_result.meta,
        )