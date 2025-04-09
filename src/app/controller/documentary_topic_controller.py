from fastapi import APIRouter, Depends, Query, Security
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.dto.request import DocumentaryTopicRequestDTO
from src.app.dto.response import (
    DocumentaryTopicResponseDTO,
    DocumentaryTopicPage,
    CurrentUserResponseDTO,
)
from src.app.schema import MessageResponse
from src.app.service.interfaces import IDocumentaryTopicService
from src.app.service.dependencies import get_documentary_topic_service, get_current_user
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/documentary-topics", tags=["Documentary Topics"])

documentary_topic_tags_metadata = {
    "name": "Documentary Topics",
    "description": "Manages documentary topics within the document management system. "
    "These topics help organize and classify documents by subject matter, "
    "enabling efficient search and retrieval of related documents. "
    "Provides CRUD operations, advanced search capabilities, and pagination features.",
}


@router.post(
    "",
    response_model=DocumentaryTopicResponseDTO,
    summary="Create a new documentary topic",
    status_code=201,
    responses={
        201: {
            "model": DocumentaryTopicResponseDTO,
            "description": "Documentary topic created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {
            "model": ConflictError,
            "description": "Documentary topic already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new documentary topic in the system. The topic name must be unique and descriptive to help"
    " with document classification.",
)
async def create_documentary_topic(
    documentary_topic_request: DocumentaryTopicRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENTARY_TOPIC_CREATE]
    ),
    documentary_topic_service: IDocumentaryTopicService = Depends(
        get_documentary_topic_service
    ),
) -> DocumentaryTopicResponseDTO:
    """
    Endpoint to create a new documentary topic.

    This endpoint allows the creation of a new documentary topic in the system. The topic data
    must be provided in the request body. If the topic is created successfully, a
    status code 201 is returned with the details of the created topic.

    :param documentary_topic_request: Request body containing the documentary topic data.
    :param current_user: The user creating the documentary topic, used for auditing and permissions.
    :param documentary_topic_service: Service that handles the documentary topic creation logic.
    :return: The data of the created documentary topic.
    """
    return await documentary_topic_service.add_documentary_topic(
        documentary_topic_request
    )


@router.get(
    "",
    response_model=list[DocumentaryTopicResponseDTO],
    summary="Get all documentary topics",
    responses={
        200: {
            "model": list[DocumentaryTopicResponseDTO],
            "description": "List of documentary topics",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete list of all documentary topics registered in the system, including their "
    "identifiers, names, and timestamps.",
)
async def get_all_documentary_topics(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENTARY_TOPIC_READ]
    ),
    documentary_topic_service: IDocumentaryTopicService = Depends(
        get_documentary_topic_service
    ),
) -> list[DocumentaryTopicResponseDTO]:
    """
    Endpoint to retrieve all documentary topics.

    This endpoint returns a list of all available documentary topics in the system. The response will include
    all topics stored in the database.

    :param current_user: The user requesting the topics, used for auditing and permissions.
    :param documentary_topic_service: Service to handle the query and retrieve all documentary topics.
    :return: A list of documentary topics in the system.
    """
    return await documentary_topic_service.get_all_documentary_topics()


@router.get(
    "/paginated",
    response_model=DocumentaryTopicPage,
    summary="Get documentary topics with pagination",
    responses={
        200: {
            "model": DocumentaryTopicPage,
            "description": "Paginated list of documentary topics",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves documentary topics in a paginated format to manage large datasets, allowing navigation "
    "through pages and control over the number of records per page.",
)
async def get_paginated_documentary_topics(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of topics per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENTARY_TOPIC_READ]
    ),
    documentary_topic_service: IDocumentaryTopicService = Depends(
        get_documentary_topic_service
    ),
) -> DocumentaryTopicPage:
    """
    Endpoint to retrieve documentary topics in a paginated manner.

    This endpoint allows retrieving documentary topics in a paginated format. The user can specify the page number
    and the number of topics per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of documentary topics to return per page.
    :param current_user: The user requesting the topics, used for auditing and permissions.
    :param documentary_topic_service: Service to handle the query and return paginated documentary topics.
    :return: A paginated list of documentary topics.
    """
    return await documentary_topic_service.get_documentary_topics_paginated(page, size)


@router.get(
    "/search",
    response_model=DocumentaryTopicPage,
    summary="Search documentary topics by term",
    responses={
        200: {
            "model": DocumentaryTopicPage,
            "description": "Paginated list of documentary topics",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs documentary topic searches based on a keyword or phrase. Results are returned paginated for "
    "better management of search results.",
)
async def find_documentary_topics(
    search_term: str | None = Query(
        None, description="Search term to filter documentary topics"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of documentary topics per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENTARY_TOPIC_READ]
    ),
    documentary_topic_service: IDocumentaryTopicService = Depends(
        get_documentary_topic_service
    ),
) -> DocumentaryTopicPage:
    """
    Endpoint to search documentary topics using a search term.

    This endpoint allows searching for documentary topics based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within documentary topic names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user performing the search, used for auditing and permissions.
    :param documentary_topic_service: Service to handle the search logic and return results.
    :return: A paginated list of documentary topics that match the search term.
    """
    return await documentary_topic_service.find(page, size, search_term)


@router.get(
    "/{documentary_topic_id}",
    response_model=DocumentaryTopicResponseDTO,
    summary="Get documentary topic by ID",
    responses={
        200: {
            "model": DocumentaryTopicResponseDTO,
            "description": "Documentary topic found",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete details of a specific documentary topic using its unique identifier.",
)
async def get_documentary_topic_by_id(
    documentary_topic_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENTARY_TOPIC_READ]
    ),
    documentary_topic_service: IDocumentaryTopicService = Depends(
        get_documentary_topic_service
    ),
) -> DocumentaryTopicResponseDTO:
    """
    Endpoint to retrieve a documentary topic by its ID.

    This endpoint retrieves the details of a specific documentary topic identified by its ID. If the topic is found,
    the topic's data is returned. If not, a 404 error is returned.

    :param documentary_topic_id: The ID of the documentary topic to retrieve.
    :param current_user: The user requesting the topic, used for auditing and permissions.
    :param documentary_topic_service: Service to handle the query and retrieve the documentary topic.
    :return: The documentary topic details.
    """
    return await documentary_topic_service.get_documentary_topic_by_id(
        documentary_topic_id
    )


@router.put(
    "/{documentary_topic_id}",
    response_model=DocumentaryTopicResponseDTO,
    summary="Update existing documentary topic",
    responses={
        200: {
            "model": DocumentaryTopicResponseDTO,
            "description": "Documentary topic updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        409: {
            "model": ConflictError,
            "description": "Documentary topic name already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing documentary topic identified by its ID. Verifies that the new name "
    "is not already in use by another topic.",
)
async def update_documentary_topic(
    documentary_topic_id: int,
    documentary_topic_request: DocumentaryTopicRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENTARY_TOPIC_UPDATE]
    ),
    documentary_topic_service: IDocumentaryTopicService = Depends(
        get_documentary_topic_service
    ),
) -> DocumentaryTopicResponseDTO:
    """
    Endpoint to update an existing documentary topic.

    This endpoint allows updating the details of an existing documentary topic identified by its ID. If the topic
    is updated successfully, the updated topic data is returned. If the topic is not found,
    a 404 error is returned.

    :param documentary_topic_id: The ID of the documentary topic to update.
    :param documentary_topic_request: The new data for the documentary topic.
    :param current_user: The user updating the topic, used for auditing and permissions.
    :param documentary_topic_service: Service to handle the update logic.
    :return: The updated documentary topic data.
    """
    return await documentary_topic_service.update_documentary_topic(
        documentary_topic_id, documentary_topic_request
    )


@router.delete(
    "/{documentary_topic_id}",
    response_model=MessageResponse,
    summary="Delete documentary topic",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Documentary topic deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Documentary topic not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific documentary topic from the system using its ID. This operation is irreversible and "
    "may affect document classifications.",
)
async def delete_documentary_topic(
    documentary_topic_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DOCUMENTARY_TOPIC_DELETE]
    ),
    documentary_topic_service: IDocumentaryTopicService = Depends(
        get_documentary_topic_service
    ),
) -> MessageResponse:
    """
    Endpoint to delete a documentary topic.

    This endpoint allows deleting a specific documentary topic identified by its ID. If the topic is deleted
    successfully, a success message is returned. If the topic is not found, a 404 error is returned.

    :param documentary_topic_id: The ID of the documentary topic to delete.
    :param current_user: The user deleting the topic, used for auditing and permissions.
    :param documentary_topic_service: Service to handle the delete logic.
    :return: A success message indicating that the documentary topic has been deleted.
    """
    return await documentary_topic_service.delete_documentary_topic(
        documentary_topic_id
    )
