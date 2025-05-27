from datetime import datetime
from fastapi import APIRouter, Depends, Query, Security, Body, Response
from src.app.exception.schema import (
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
from src.app.schema import MessageResponse
from src.app.service.interfaces import IDocumentCategoryService
from src.app.service.dependencies import get_document_category_service, get_current_user
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/document-categories", tags=["Document Categories"])

document_category_tags_metadata = {
    "name": "Document Categories",
    "description": "Manages document category classifications within the system. "
    "These categories help organize and classify different types of documents, "
    "enabling efficient search and retrieval of related documents. "
    "Provides CRUD operations, advanced search capabilities, and pagination features.",
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
    description="Creates a new document category in the system. The category name must be unique and contain only "
    "alphabetic characters.",
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
    description="Retrieves the complete list of all document categories registered in the system, including their "
    "identifiers, names, and timestamps.",
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
    description="Retrieves document categories in a paginated format to manage large data sets, allowing navigation "
    "through pages and control over the number of records per page.",
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
    description="Performs document category searches based on a keyword or phrase. Results are returned paginated for "
    "better management of search results.",
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
    description="Deletes multiple document categories from the system using a list of IDs. This operation is "
    "irreversible and may affect document classifications. All specified categories must exist for the "
    "operation to succeed.",
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
    description="Retrieves the complete details of a specific document category using its unique identifier.",
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
    description="Updates the details of an existing document category identified by its ID. Verifies that the new name "
    "is not already in use by another category.",
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
    description="Deletes a specific document category from the system using its ID. This operation is irreversible and "
    "may affect document classifications.",
)
async def delete_document_category(
    document_category_id: int,
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
        document_category_id
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
    description="Exports document categories to an Excel file. If category IDs are provided, only those specific "
    "categories will be exported. If no IDs are provided, all categories will be exported. The Excel file "
    "includes formatted columns with proper headers and styling.",
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
