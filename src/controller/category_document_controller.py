from fastapi import APIRouter, Depends, Query
from src.exception.schema import BackRequestError, ConflictError, InternalServerError, NotFoundError
from src.dto.request import CategoryDocumentRequestDTO
from src.dto.response import CategoryDocumentResponseDTO, CategoryDocumentPage
from src.service.dependencies import get_category_document_service
from src.service.interfaces import ICategoryDocumentService

router = APIRouter(prefix="/category", tags=["Category Document"])

category_document_tags_metadata = {
    "name": "Category Document",
    "description": "Operations with category documents",
}

@router.get(
    "",
    status_code=200,
    response_model=list[CategoryDocumentResponseDTO],
    responses={
        200: {"model": list[CategoryDocumentResponseDTO], "description": "List of document categories"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Get all document categories",
)
async def get_all_category_documents(
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> list[CategoryDocumentResponseDTO]:
    """
    Get all document categories.

    :param category_document_service: Service to handle the query
    :return: List of document categories
    """
    return await category_document_service.get_all_categories_documents()


@router.get(
    "/{category_document_id}",
    status_code=200,
    response_model=CategoryDocumentResponseDTO,
    responses={
        200: {"model": CategoryDocumentResponseDTO, "description": "Document category found"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Get document category by ID",
)
async def get_category_document_by_id(
    category_document_id: int,
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentResponseDTO:
    """
    Get a document category by its ID.

    :param category_document_id: ID of the document category
    :param category_document_service: Service to handle the query
    :return: The document category found
    """
    return await category_document_service.get_category_document_by_id(category_document_id)


@router.put(
    "/{category_document_id}",
    status_code=200,
    response_model=CategoryDocumentResponseDTO,
    responses={
        200: {"model": CategoryDocumentResponseDTO, "description": "Document category successfully updated"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        409: {"model": ConflictError, "description": "Document category already exists"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Update document category",
)
async def update_category_document(
    category_document_id: int,
    category_document: CategoryDocumentRequestDTO,
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentResponseDTO:
    """
    Update an existing document category.

    :param category_document_id: ID of the document category
    :param category_document: Updated document category data
    :param category_document_service: Service to handle the update
    :return: The updated document category
    """
    return await category_document_service.update_category_document(category_document_id, category_document)


@router.delete(
    "/{category_document_id}",
    status_code=200,
    responses={
        200: {"description": "Document category successfully deleted"},
        404: {"model": NotFoundError, "description": "Document category not found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Delete document category",
)
async def delete_category_document(
    category_document_id: int,
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
):
    """
    Delete a document category by its ID.

    :param category_document_id: ID of the document category to delete
    :param category_document_service: Service to handle the deletion
    :return: Confirmation message
    """
    return await category_document_service.delete_category_document(category_document_id)


@router.get(
    "/paginated/",
    status_code=200,
    response_model=CategoryDocumentPage,
    responses={
        200: {"model": CategoryDocumentPage, "description": "Paginated list of document categories"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Get paginated document categories",
)
async def get_paginated_category_documents(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, description="Page size"),
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentPage:
    """
    Get document categories with pagination.

    :param page: Page number
    :param size: Page size
    :param category_document_service: Service to handle the query
    :return: Paginated list of document categories
    """
    return await category_document_service.get_paginated_category_documents(page, size)


@router.get(
    "/search/",
    status_code=200,
    response_model=CategoryDocumentPage,
    responses={
        200: {"model": CategoryDocumentPage, "description": "Document categories search results"},
        404: {"model": NotFoundError, "description": "No document categories found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search document categories",
)
async def find_category_documents(
    search_term: str = Query(..., description="Search term"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, description="Page size"),
    category_document_service: ICategoryDocumentService = Depends(get_category_document_service),
) -> CategoryDocumentPage:
    """
    Search document categories with a search term.

    :param search_term: Term to search for
    :param page: Page number
    :param size: Page size
    :param category_document_service: Service to handle the search
    :return: Paginated search results
    """
    return await category_document_service.find(page, size, search_term)