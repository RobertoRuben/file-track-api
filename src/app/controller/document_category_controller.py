from datetime import datetime
from fastapi import APIRouter, Depends, Query, Security, Body, Response, Request
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.dto.request import DocumentCategoryRequestDTO
from src.app.dto.response import (
    DocumentCategoryResponseDTO,
    DocumentCategoryPage,
    CurrentUserResponseDTO,
)
from src.app.core.schema import MessageResponse
from src.app.service.interfaces import IDocumentCategoryService
from src.app.service.dependencies import get_document_category_service, get_current_user
from src.app.core.security.auth import Scopes

router = APIRouter(prefix="/document-categories", tags=["Document Categories"])

document_category_tags_metadata = {
    "name": "Document Categories",
    "description": "Comprehensive enterprise document classification system managing taxonomic structures, "
    "organizational categorization, and semantic document organization for enhanced information management "
    "and retrieval efficiency. Facilitates systematic document organization through hierarchical category "
    "management, automated classification workflows, and advanced search optimization supporting enterprise "
    "content management, regulatory compliance, and knowledge management systems. Enables structured document "
    "lifecycle administration with sophisticated categorization capabilities for organizational information "
    "governance and enhanced document discoverability across enterprise environments.",
}


@router.post(
    "",
    response_model=DocumentCategoryResponseDTO,
    summary="Create a new document category",
    status_code=201,
    responses={
        201: {
            "model": DocumentCategoryResponseDTO,
            "description": "Document category created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {
            "model": ConflictError,
            "description": "Document category already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new document category in the system to organize and classify document types effectively. "
    "The category name must be unique across the entire system and follows specific validation rules including "
    "alphabetic character constraints. This endpoint establishes a new classification structure that can be "
    "used to categorize documents for improved organization, searchability, and management. The created category "
    "becomes immediately available for document assignment and filtering operations throughout the system.",
)
async def create_document_category(
    document_category_request: DocumentCategoryRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_CREATE]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> DocumentCategoryResponseDTO:
    """
    Endpoint to create a new document category.

    This endpoint allows the creation of a new document category in the system. The category data
    must be provided in the request body. If the category is created successfully, a
    status code 201 is returned with the details of the created category.

    :param document_category_request: Request body containing the document category data.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service that handles the document category creation logic.
    :return: The data of the created document category.
    """
    return await document_category_service.add_document_category(
        document_category_request
    )


@router.get(
    "",
    response_model=list[DocumentCategoryResponseDTO],
    summary="Get all document categories",
    responses={
        200: {
            "model": list[DocumentCategoryResponseDTO],
            "description": "List of document categories",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a comprehensive collection of all document categories registered in the system. "
    "This endpoint returns complete category information including unique identifiers, names, descriptions, "
    "creation timestamps, and modification dates. The response provides the complete taxonomy of document "
    "classifications available for organizing and categorizing documents. This data is essential for "
    "populating category selection interfaces, implementing document filtering systems, and maintaining "
    "administrative oversight of the classification structure.",
)
async def get_all_document_categories(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_READ]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> list[DocumentCategoryResponseDTO]:
    """
    Endpoint to retrieve all document categories.

    This endpoint returns a list of all available document categories in the system. The response will include
    all categories stored in the database.

    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the query and retrieve all document categories.
    :return: A list of document categories in the system.
    """
    return await document_category_service.get_all_document_categories()


@router.get(
    "/paginated",
    response_model=DocumentCategoryPage,
    summary="Get document categories with pagination",
    responses={
        200: {
            "model": DocumentCategoryPage,
            "description": "Paginated list of document categories",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides document categories through an efficient pagination system designed for handling large "
    "category collections with optimal performance. This endpoint returns structured page metadata including "
    "total record counts, total pages, current page indicators, and navigation flags (hasNext, hasPrevious) "
    "to support sophisticated user interface components. The pagination approach significantly improves "
    "application responsiveness when dealing with extensive category hierarchies and enables smooth "
    "navigation through large datasets in administrative interfaces and category selection controls.",
)
async def get_paginated_document_categories(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of categories per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_READ]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> DocumentCategoryPage:
    """
    Endpoint to retrieve document categories in a paginated manner.

    This endpoint allows retrieving document categories in a paginated format. The user can specify the page number
    and the number of categories per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of document categories to return per page.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the query and return paginated document categories.
    :return: A paginated list of document categories.
    """
    return await document_category_service.get_paginated_document_categories(page, size)


@router.get(
    "/search",
    response_model=DocumentCategoryPage,
    summary="Search document categories by term",
    responses={
        200: {
            "model": DocumentCategoryPage,
            "description": "Paginated list of document categories",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Implements intelligent search capabilities across document categories using flexible text matching "
    "algorithms. This endpoint performs case-insensitive partial matching against category names and descriptions, "
    "enabling users to quickly locate specific categories or groups of related categories. The search functionality "
    "supports dynamic filtering as users type, making it ideal for implementing auto-complete features, "
    "advanced filtering systems, and category discovery tools. Results are delivered in paginated format "
    "with configurable page sizes to maintain optimal performance regardless of search result volume.",
)
async def find_document_categories(
    search_term: str | None = Query(
        None, description="Search term to filter document categories"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of document categories per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_READ]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> DocumentCategoryPage:
    """
    Endpoint to search document categories using a search term.

    This endpoint allows searching for document categories based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within document category names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the search logic and return results.
    :return: A paginated list of document categories that match the search term.
    """
    return await document_category_service.find(page, size, search_term)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple document categories",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Document categories deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "One or more document categories not found",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes bulk deletion of multiple document categories in a single atomic transaction to maintain "
    "data consistency and system integrity. This endpoint accepts a collection of category identifiers and "
    "removes all corresponding categories from the system simultaneously. The operation follows an all-or-nothing "
    "approach - if any category cannot be deleted due to constraints or dependencies, the entire operation "
    "is rolled back to prevent partial deletions. Before execution, the system validates category existence, "
    "checks for document associations, and verifies user permissions. This operation permanently affects "
    "document classification structures and may impact existing document categorizations throughout the system.",
)
async def delete_document_categories_bulk(
    category_ids: list[int] = Body(
        ..., description="List of document category IDs to delete"
    ),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_DELETE]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> MessageResponse:
    """
    Endpoint to delete multiple document categories.

    This endpoint allows deleting multiple document categories identified by their IDs. If all categories
    are deleted successfully, a success message is returned. If any category is not found, a 404 error
    is returned. The request body should contain a list of document category IDs.

    :param category_ids: List of document category IDs to delete.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the bulk delete logic.
    :return: A success message indicating that the document categories have been deleted.
    """
    return await document_category_service.delete_document_categories_by_ids(
        category_ids
    )


@router.post(
    "/export-excel",
    summary="Export document categories to Excel",
    responses={
        200: {
            "description": "Excel file with document categories",
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "One or more document categories not found",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates professionally formatted Excel spreadsheets containing comprehensive document category data "
    "for reporting, analysis, and administrative purposes. This endpoint creates optimized Excel files with "
    "properly structured columns, formatted headers, and enhanced styling for improved readability. Users can "
    "specify particular categories for targeted exports or export the complete category collection. The generated "
    "files include detailed category information such as names, descriptions, usage statistics, creation dates, "
    "and modification timestamps. Files are automatically named with timestamps to ensure uniqueness and provide "
    "audit trails. This functionality supports data backup procedures, regulatory compliance reporting, and "
    "stakeholder communication requirements.",
)
async def export_document_categories_to_excel(
    category_ids: list[int] = Body(
        ...,
        description="List of document category IDs to export. If empty, exports all categories",
    ),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_READ]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> Response:
    """
    Endpoint to export document categories to Excel format.

    This endpoint generates an Excel file containing document category data. Users can specify which
    categories to export by providing a list of IDs, or export all categories if no IDs are provided.
    The Excel file includes proper formatting, headers, and is returned as a downloadable stream.

    :param category_ids: Optional list of document category IDs to export. If None, exports all categories.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the Excel export logic.
    :return: A StreamingResponse containing the Excel file for download.
    """
    excel_data = await document_category_service.export_document_categories_to_excel(
        category_ids
    )

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return Response(
        content=excel_data,
        headers=headers,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get(
    "/{document_category_id}",
    response_model=DocumentCategoryResponseDTO,
    summary="Get document category by ID",
    responses={
        200: {
            "model": DocumentCategoryResponseDTO,
            "description": "Document category found",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive details of a specific document category using its unique system identifier. "
    "This endpoint returns complete category information including the category name, detailed description, "
    "creation timestamp, last modification date, usage statistics, and associated metadata. The category ID "
    "must correspond to an existing category in the system. This endpoint is essential for displaying detailed "
    "category information in administrative interfaces, populating category edit forms, and providing context "
    "for document classification operations. The returned data supports various UI components and business "
    "logic that depends on specific category characteristics.",
)
async def get_document_category_by_id(
    document_category_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_READ]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> DocumentCategoryResponseDTO:
    """
    Endpoint to retrieve a document category by its ID.

    This endpoint retrieves the details of a specific document category identified by its ID. If the category is found,
    the category's data is returned. If not, a 404 error is returned.

    :param document_category_id: The ID of the document category to retrieve.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the query and retrieve the document category.
    :return: The document category details.
    """
    return await document_category_service.get_document_category_by_id(
        document_category_id
    )


@router.put(
    "/{document_category_id}",
    response_model=DocumentCategoryResponseDTO,
    summary="Update existing document category",
    responses={
        200: {
            "model": DocumentCategoryResponseDTO,
            "description": "Document category updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        409: {
            "model": ConflictError,
            "description": "Document category name already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the properties and metadata of an existing document category while maintaining system "
    "integrity and data consistency. This endpoint allows modification of category attributes such as name "
    "and description, with comprehensive validation to ensure the updated name remains unique across the "
    "entire category system (excluding the current category being modified). The system performs thorough "
    "validation of input data, checks for naming conflicts, and automatically updates modification timestamps. "
    "Changes are immediately reflected throughout the system, affecting document classification displays and "
    "category selection interfaces. This operation is crucial for maintaining an organized and up-to-date "
    "document classification taxonomy.",
)
async def update_document_category(
    document_category_id: int,
    document_category_request: DocumentCategoryRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_UPDATE]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> DocumentCategoryResponseDTO:
    """
    Endpoint to update an existing document category.

    This endpoint allows updating the details of an existing document category identified by its ID. If the category
    is updated successfully, the updated category data is returned. If the category is not found,
    a 404 error is returned.

    :param document_category_id: The ID of the document category to update.
    :param document_category_request: The new data for the document category.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the update logic.
    :return: The updated document category data.
    """
    return await document_category_service.update_document_category(
        document_category_id, document_category_request
    )


@router.delete(
    "/{document_category_id}",
    response_model=MessageResponse,
    summary="Delete document category",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Document category deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Permanently removes a specific document category from the system using its unique identifier, "
    "with comprehensive impact assessment and validation. This irreversible operation completely eliminates "
    "the category and all its associated metadata from the database. Prior to deletion, the system performs "
    "thorough checks for existing document associations and dependencies to prevent data integrity violations. "
    "Documents currently classified under this category may be affected by this operation, potentially requiring "
    "recategorization or becoming unclassified. This endpoint requires elevated privileges and should be used "
    "with extreme caution in production environments. The operation supports administrative cleanup of obsolete "
    "categories and taxonomy restructuring initiatives.",
)
async def delete_document_category(
    document_category_id: int,
    request: Request,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENT_CATEGORY_DELETE]
    ),
    document_category_service: IDocumentCategoryService = Depends(
        get_document_category_service
    ),
) -> MessageResponse:
    """
    Endpoint to delete a document category.

    This endpoint allows deleting a specific document category identified by its ID. If the category is deleted
    successfully, a success message is returned. If the category is not found, a 404 error is returned.

    :param document_category_id: The ID of the document category to delete.
    :param current_user: The current user making the request, used for authorization.
    :param document_category_service: Service to handle the delete logic.
    :return: A success message indicating that the document category has been deleted.
    """
    return await document_category_service.delete_document_category(
        document_category_id, request
    )
