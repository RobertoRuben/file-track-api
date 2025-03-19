from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import BackRequestError, ConflictError, InternalServerError, NotFoundError
from src.app.dto.request import CategoryDocumentRequestDTO
from src.app.dto.response import CategoryDocumentResponseDTO, CategoryDocumentPage
from src.app.schema import MessageResponse
from src.app.service.dependencies import get_category_document_service
from src.app.service.interfaces import ICategoryDocumentService

router = APIRouter(
    prefix="/category",
    tags=["Category Document"]
)

category_document_tags_metadata = {
    "name": "Category Document",
    "description": "Manage document classification categories in the system. Includes endpoints for creating, "
                   "retrieving, updating, and deleting document categories, as well as advanced search and pagination "
                   "capabilities for efficient data management.",
}

@router.get(
    "",
    response_model=list[CategoryDocumentResponseDTO],
    summary="Get all document categories",
    responses={
        200: {"model": list[CategoryDocumentResponseDTO], "description": "List of document categories"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve all document categories in the system.",
)
async def get_all_category_documents(
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> list[CategoryDocumentResponseDTO]:
    """
    Retrieve all document categories available in the system.

    This endpoint fetches all the document categories stored in the system and returns them in a list format.

    :param category_document_service: Service to handle the query and return all document categories.
    :return: A list of document categories.
    """
    return await category_document_service.get_all_categories_documents()


@router.post(
    "",
    status_code=201,
    response_model=CategoryDocumentResponseDTO,
    summary="Create a new document category in the system",
    responses={
        201: {"model": CategoryDocumentResponseDTO, "description": "Document category successfully created"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {"model": ConflictError, "description": "Document category already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Create a new document category in the system. Provide the necessary details to create a new category.",
)
async def create_category_document(
    category_document_request: CategoryDocumentRequestDTO,
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentResponseDTO:
    """
    Create a new document category in the system.

    This endpoint allows for the creation of a new document category by providing the necessary details.

    :param category_document_request: The data required to create a new document category.
    :param category_document_service: Service to handle the creation logic.
    :return: The created document category's details.
    """
    return await category_document_service.add_category_document(category_document_request)


@router.get(
    "/paginated/",
    response_model=CategoryDocumentPage,
    summary="Get paginated document categories",
    responses={
        200: {"model": CategoryDocumentPage, "description": "Paginated list of document categories"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Get a paginated list of document categories.",
)
async def get_paginated_category_documents(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, description="Page size"),
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentPage:
    """
    Retrieve document categories in a paginated format.

    This endpoint allows for fetching document categories in a paginated manner, where the user specifies
    the page number and the page size to optimize data retrieval.

    :param page: The page number to retrieve.
    :param size: The number of document categories per page.
    :param category_document_service: Service to handle the query and return the paginated categories.
    :return: A paginated list of document categories.
    """
    return await category_document_service.get_paginated_category_documents(page, size)


@router.get(
    "/search/",
    response_model=CategoryDocumentPage,
    summary="Search for categories documents based on a search term.",
    responses={
        200: {"model": CategoryDocumentPage, "description": "Document categories search results"},
        404: {"model": NotFoundError, "description": "No document categories found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search document categories based on a search term.",
)
async def find_category_documents(
    search_term: str = Query(..., description="Search term"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, description="Page size"),
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentPage:
    """
    Search for document categories based on a search term.

    This endpoint allows users to search document categories based on a provided search term, with pagination
    to manage large results.

    :param search_term: The term to search for within document categories.
    :param page: The page number to retrieve.
    :param size: The number of categories per page.
    :param category_document_service: Service to handle the search logic.
    :return: A paginated list of document categories matching the search term.
    """
    return await category_document_service.find(page, size, search_term)


@router.get(
    "/{category_document_id}",
    response_model=CategoryDocumentResponseDTO,
    summary="Get a document category by ID",
    responses={
        200: {"model": CategoryDocumentResponseDTO, "description": "Document category found"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve a specific document category by its ID.",
)
async def get_category_document_by_id(
    category_document_id: int,
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentResponseDTO:
    """
    Retrieve a document category by its unique ID.

    This endpoint fetches the document category identified by the provided ID and returns its details.

    :param category_document_id: The unique ID of the document category to retrieve.
    :param category_document_service: Service to handle the query and return the document category.
    :return: The details of the document category.
    """
    return await category_document_service.get_category_document_by_id(category_document_id)


@router.put(
    "/{category_document_id}",
    response_model=CategoryDocumentResponseDTO,
    summary="Update document category",
    responses={
        200: {"model": CategoryDocumentResponseDTO, "description": "Document category successfully updated"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        409: {"model": ConflictError, "description": "Document category already exists"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Update the details of an existing document category.",
)
async def update_category_document(
    category_document_id: int,
    category_document: CategoryDocumentRequestDTO,
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentResponseDTO:
    """
    Update an existing document category with the provided data.

    This endpoint allows for the modification of an existing document category. It requires the document
    category ID and the updated details to process the update.

    :param category_document_id: The unique ID of the document category to update.
    :param category_document: The updated data for the document category.
    :param category_document_service: Service to handle the update process.
    :return: The updated document category's details.
    """
    return await category_document_service.update_category_document(category_document_id, category_document)


@router.delete(
    "/{category_document_id}",
    response_model=MessageResponse,
    summary="Delete document category",
    responses={
        200: {"description": "Document category successfully deleted"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Delete a document category from the system by its ID.",
)
async def delete_category_document(
    category_document_id: int,
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
):
    """
    Delete a document category identified by its ID.

    This endpoint allows for the deletion of a document category from the system based on its ID.

    :param category_document_id: The unique ID of the document category to delete.
    :param category_document_service: Service to handle the deletion logic.
    :return: A success message indicating the deletion.
    """
    return await category_document_service.delete_category_document(category_document_id)





