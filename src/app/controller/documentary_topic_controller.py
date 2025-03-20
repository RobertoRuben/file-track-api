from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError
)
from src.app.dto.request import DocumentaryTopicRequestDTO
from src.app.dto.response import DocumentaryTopicResponseDTO, DocumentaryTopicPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IDocumentaryTopicService
from src.app.service.dependencies import get_documentary_topic_service

router = APIRouter(
    prefix="/documentary-topic",
    tags=["DocumentaryTopic"]
)

documentary_topic_tags_metadata = {
    "name": "DocumentaryTopic",
    "description": "Manages documentary topics within the system. These operations allow creating, retrieving, "
                   "updating, and deleting documentary topics, as well as searching and listing them with pagination.",
}

@router.post(
    "",
    response_model=DocumentaryTopicResponseDTO,
    summary="Create a new documentary topic in the system",
    status_code=201,
    responses={
        201: {"model": DocumentaryTopicResponseDTO, "description": "Documentary topic created successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {"model": ConflictError, "description": "Documentary topic already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new documentary topic in the system. Provide the documentary topic details in the request body to create it successfully.",
)
async def create_documentary_topic(
    documentary_topic_request: DocumentaryTopicRequestDTO,
    documentary_topic_service: IDocumentaryTopicService = Depends(get_documentary_topic_service),
) -> DocumentaryTopicResponseDTO:
    """
    Endpoint to create a new documentary topic.

    This endpoint allows the creation of a new documentary topic in the system. The documentary topic data
    must be provided in the request body. If the documentary topic is created successfully, a status code 201
    with the created documentary topic's details is returned.

    :param documentary_topic_request: Request body containing documentary topic data.
    :param documentary_topic_service: Service to handle the documentary topic creation logic.
    :return: The created documentary topic data.
    """
    return await documentary_topic_service.add_documentary_topic(documentary_topic_request)


@router.get(
    "",
    response_model=list[DocumentaryTopicResponseDTO],
    summary="Get all documentary topics",
    responses={
        200: {"model": list[DocumentaryTopicResponseDTO], "description": "List of documentary topics"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a list of all documentary topics in the system.",
)
async def get_all_documentary_topics(
    documentary_topic_service: IDocumentaryTopicService = Depends(get_documentary_topic_service),
) -> list[DocumentaryTopicResponseDTO]:
    """
    Endpoint to retrieve all documentary topics.

    This endpoint returns a list of all available documentary topics in the system. The response will include
    all documentary topics stored in the database.

    :param documentary_topic_service: Service to handle the query and retrieve all documentary topics.
    :return: A list of documentary topics in the system.
    """
    return await documentary_topic_service.get_all_documentary_topics()


@router.get(
    "/paginated",
    response_model=DocumentaryTopicPage,
    summary="Get documentary topics with pagination",
    responses={
        200: {"model": DocumentaryTopicPage, "description": "Paginated list of documentary topics"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves documentary topics in a paginated format to manage large data sets.",
)
async def get_paginated_documentary_topics(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of documentary topics per page"),
    documentary_topic_service: IDocumentaryTopicService = Depends(get_documentary_topic_service),
) -> DocumentaryTopicPage:
    """
    Endpoint to retrieve documentary topics in a paginated manner.

    This endpoint allows retrieving documentary topics in a paginated format. The user can specify the page number
    and the number of documentary topics per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of documentary topics to return per page.
    :param documentary_topic_service: Service to handle the query and return paginated documentary topics.
    :return: A paginated list of documentary topics.
    """
    return await documentary_topic_service.get_documentary_topics_paginated(page, size)


@router.get(
    "/search",
    response_model=DocumentaryTopicPage,
    summary="Search documentary topics based on a term",
    responses={
        200: {"model": DocumentaryTopicPage, "description": "Paginated list of documentary topics"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search documentary topics based on a keyword or phrase, with pagination for better management of search results.",
)
async def find_documentary_topics(
    search_term: str | None = Query(None, description="Search term to filter documentary topics"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of documentary topics per page"),
    documentary_topic_service: IDocumentaryTopicService = Depends(get_documentary_topic_service),
) -> DocumentaryTopicPage:
    """
    Endpoint to search documentary topics using a search term.

    This endpoint allows searching for documentary topics based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within documentary topic names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param documentary_topic_service: Service to handle the search logic and return results.
    :return: A paginated list of documentary topics that match the search term.
    """
    return await documentary_topic_service.find(page, size, search_term)


@router.get(
    "/{documentary_topic_id}",
    response_model=DocumentaryTopicResponseDTO,
    summary="Get a specific documentary topic by ID",
    responses={
        200: {"model": DocumentaryTopicResponseDTO, "description": "Documentary topic found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific documentary topic using its ID.",
)
async def get_documentary_topic_by_id(
    documentary_topic_id: int,
    documentary_topic_service: IDocumentaryTopicService = Depends(get_documentary_topic_service),
) -> DocumentaryTopicResponseDTO:
    """
    Endpoint to retrieve a documentary topic by its ID.

    This endpoint retrieves the details of a specific documentary topic identified by its ID. If the documentary topic is found,
    the documentary topic's data is returned. If not, a 404 error is returned.

    :param documentary_topic_id: The ID of the documentary topic to retrieve.
    :param documentary_topic_service: Service to handle the query and retrieve the documentary topic.
    :return: The documentary topic details.
    """
    return await documentary_topic_service.get_documentary_topic_by_id(documentary_topic_id)


@router.put(
    "/{documentary_topic_id}",
    response_model=DocumentaryTopicResponseDTO,
    summary="Update an existing documentary topic by ID",
    responses={
        200: {"model": DocumentaryTopicResponseDTO, "description": "Documentary topic updated successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing documentary topic by its ID.",
)
async def update_documentary_topic(
    documentary_topic_id: int,
    documentary_topic_request: DocumentaryTopicRequestDTO,
    documentary_topic_service: IDocumentaryTopicService = Depends(get_documentary_topic_service),
) -> DocumentaryTopicResponseDTO:
    """
    Endpoint to update an existing documentary topic.

    This endpoint allows updating the details of an existing documentary topic identified by its ID. If the documentary topic
    is updated successfully, the updated documentary topic data is returned. If the documentary topic is not found,
    a 404 error is returned.

    :param documentary_topic_id: The ID of the documentary topic to update.
    :param documentary_topic_request: The new data for the documentary topic.
    :param documentary_topic_service: Service to handle the update logic.
    :return: The updated documentary topic data.
    """
    return await documentary_topic_service.update_documentary_topic(documentary_topic_id, documentary_topic_request)


@router.delete(
    "/{documentary_topic_id}",
    response_model=MessageResponse,
    summary="Delete a documentary topic by ID",
    responses={
        200: {"model": MessageResponse, "description": "Documentary topic deleted successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific documentary topic from the system using its ID.",
)
async def delete_documentary_topic(
    documentary_topic_id: int,
    documentary_topic_service: IDocumentaryTopicService = Depends(get_documentary_topic_service),
) -> MessageResponse:
    """
    Endpoint to delete a documentary topic.

    This endpoint allows deleting a specific documentary topic identified by its ID. If the documentary topic is deleted
    successfully, a success message is returned. If the documentary topic is not found, a 404 error is returned.

    :param documentary_topic_id: The ID of the documentary topic to delete.
    :param documentary_topic_service: Service to handle the delete logic.
    :return: A success message indicating that the documentary topic has been deleted.
    """
    return await documentary_topic_service.delete_documentary_topic(documentary_topic_id)