import io
import pandas as pd
from datetime import datetime
from src.app.model.entity import DocumentCategory
from src.app.core.helpers import datetime_helper
from src.app.domain.document.dto import DocumentCategoryRequestDTO
from src.app.domain.document.dto import (
    DocumentCategoryPage,
    DocumentCategoryResponseDTO,
)
from src.app.core.schema import MessageResponse
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.core.exception import handle_exceptions
from src.app.domain.document.repository.interface import IDocumentCategoryRepository
from src.app.domain.document.service.interfaces import IDocumentCategoryService


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
                message="Document category already exists",
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
                message="Document category not found",
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
                    message="Document category name already exists",
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
        self, document_category_id: int, request
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
                message="Document category not found",
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
                message="Document category not found",
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
                message="Invalid page size",
                details="Page size must be greater than 0.",
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
        Find document categories by search term with pagination.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_term: The search term to filter document categories
        :return: A DocumentCategoryPage with document categories matching the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no document categories match the search criteria
        """
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid page size",
                details="Page size must be greater than 0.",
            )

        search_dict = {}
        if search_term and search_term.strip():
            search_dict["name"] = search_term.strip()

        page_result = await self.document_category_repository.find(
            page=page, size=size, search_dict=search_dict
        )

        if not page_result.data:
            raise NotFoundException(
                message="No document categories found",
                details=f"No document categories found matching the search term '{search_term}'.",
            )

        document_categories_response = [
            DocumentCategoryResponseDTO(
                id=category.id,
                name=category.name,
                created_at=category.created_at,
                updated_at=category.updated_at,
            )
            for category in page_result.data
        ]

        return DocumentCategoryPage(
            data=document_categories_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def delete_document_categories_by_ids(
        self, category_ids: list[int]
    ) -> MessageResponse:
        """
        Delete multiple document categories by their IDs.

        :param category_ids: List of document category IDs to delete
        :return: A MessageResponse indicating the result of the deletion
        :raises NotFoundException: If none of the document categories with the given IDs exist
        :raises BadRequestException: If the category_ids list is empty
        """
        if len(category_ids) == 0:
            raise BadRequestException(
                message="No document category IDs provided",
                details="Please provide a list of document category IDs to delete.",
            )

        invalid_ids = [id for id in category_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid document category IDs",
                details=f"Document category IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        document_categories = await self.document_category_repository.find_by_ids(
            category_ids
        )

        found_ids = {
            category["id"] if isinstance(category, dict) else category.id
            for category in document_categories
        }
        missing_ids = [id for id in category_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Document categories not found",
                details=f"Document categories with IDs {missing_ids} not found. Cannot proceed with deletion.",
            )

        resp = await self.document_category_repository.delete_by_ids(category_ids)

        if resp is True:
            return MessageResponse(
                message="Document categories deleted successfully.",
                success=True,
                details=f"Document categories with IDs {category_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete document categories.",
                success=False,
                details=f"Document categories with IDs {category_ids} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def export_document_categories_to_excel(
        self, category_ids: list[int]
    ) -> bytes:
        """
        Export document categories to Excel format.

        :param category_ids: List of document category IDs to export. If empty, exports all categories
        :return: Excel file content as bytes
        :raises NotFoundException: If none of the document categories with the given IDs exist
        :raises BadRequestException: If the category_ids list is empty or contains invalid IDs
        """

        if len(category_ids) == 0:
            raise BadRequestException(
                message="No document category IDs provided",
                details="Please provide a list of document category IDs to export.",
            )

        invalid_ids = [id for id in category_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid document category IDs",
                details=f"Document category IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        document_categories = await self.document_category_repository.find_by_ids(
            category_ids
        )

        found_ids = {
            category["id"] if isinstance(category, dict) else category.id
            for category in document_categories
        }

        missing_ids = [id for id in category_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Document categories not found",
                details=f"Document categories with IDs {missing_ids} not found. Cannot proceed with export.",
            )

        categories_data = [
            {
                "ID": category.id,
                "Nombre": category.name,
                "Fecha de Creación": datetime_helper.to_lima_timezone(
                    category.created_at
                ),
                "Fecha de Actualización": datetime_helper.to_lima_timezone(
                    category.updated_at
                ),
            }
            for category in document_categories
        ]

        df = pd.DataFrame(categories_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Document Categories")

            worksheet = writer.sheets["Document Categories"]
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_length)

        output.seek(0)
        return output.getvalue()
