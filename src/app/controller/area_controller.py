from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import AreaConnectionRequestDto
from src.app.dto.response import AreaConnectionResponseDTO, AreaConnectionPage
from src.app.schema import MessageResponse
from src.app.service.dependencies import get_area_connection_service
from src.app.service.interfaces import IAreaConnectionService

router = APIRouter(prefix="/area-connections", tags=["Department Connections"])

area_connection_tags_metadata = {
    "name": "Department Connections",
    "description": "Manage connections between different departments in the system. This includes creating, "
    "updating, deleting, and retrieving connections between departments.",
}


@router.post(
    "/",
    response_model=AreaConnectionResponseDTO,
    summary="Create a new area connection",
    responses={
        200: {
            "model": AreaConnectionResponseDTO,
            "description": "Area connection created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {"model": ConflictError, "description": "Area connection already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Create a new area connection in the system.",
)
async def create_area_connection(
    area_connection: AreaConnectionRequestDto,
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> AreaConnectionResponseDTO:
    """
    Create a new area connection.

    Args:
        area_connection (AreaConnectionRequestDto): The area connection to create.
        area_connection_service (IAreaConnectionService, optional): The area connection service. Defaults to Depends(get_area_connection_service).

    Returns:
        AreaConnectionResponseDTO: The created area connection.
    """
    return await area_connection_service.add_area_connection(area_connection)


@router.get(
    "/",
    response_model=list[AreaConnectionResponseDTO],
    summary="Get all area connections",
    responses={
        200: {
            "model": list[AreaConnectionResponseDTO],
            "description": "List of area connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve a list of all area connections in the system.",
)
async def get_all_area_connections(
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> list[AreaConnectionResponseDTO]:
    """
    Endpoint to retrieve all area connections.

    This endpoint returns a list of all area connections available in the system. The response will include
    all area connections stored in the database.

    :param area_connection_service: Service to handle the query and retrieve all area connections.
    :return: A list of area connections in the system.
    """
    return await area_connection_service.get_all_area_connections()


@router.get(
    "/paginated",
    response_model=AreaConnectionPage,
    summary="Get area connections with pagination",
    responses={
        200: {
            "model": AreaConnectionPage,
            "description": "Paginated list of area connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve area connections in a paginated format to manage large datasets.",
)
async def get_paginated_area_connections(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of area connections per page"),
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> AreaConnectionPage:
    """
    Endpoint to retrieve area connections in a paginated manner.

    This endpoint allows for retrieving area connections in a paginated format. The user can specify the page
    number and the number of area connections per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of area connections to return per page.
    :param area_connection_service: Service to handle the query and return paginated area connections.
    :return: A paginated list of area connections.
    """
    return await area_connection_service.get_paginated_area_connections(page, size)


@router.get(
    "/search",
    response_model=AreaConnectionPage,
    summary="Search area connections by term",
    responses={
        200: {
            "model": AreaConnectionPage,
            "description": "Paginated list of connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Connection not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Search area connections based on a keyword, with pagination to manage results.",
)
async def find_area_connections(
    search_term: str | None = Query(
        None, description="Search term to filter connections"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of connections per page"),
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> AreaConnectionPage:
    """
    Endpoint to search area connections using a search term.

    This endpoint allows searching for area connections based on a given term. Results are returned in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: Term to search for in the area connection details.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param area_connection_service: Service to handle the search logic and return the results.
    :return: A paginated list of area connections that match the search term.
    """
    return await area_connection_service.find(page, size, search_term)


@router.get(
    "/{area_connection_id}",
    response_model=AreaConnectionResponseDTO,
    summary="Get area connection by ID",
    responses={
        200: {
            "model": AreaConnectionResponseDTO,
            "description": "Area connection found",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Area connection not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieve details of a specific area connection using its ID.",
)
async def get_area_connection_by_id(
    area_connection_id: int,
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> AreaConnectionResponseDTO:
    """
    Endpoint to retrieve an area connection by its ID.

    This endpoint retrieves the details of a specific area connection identified by its ID. If found, it returns the connection data. If not, it returns a 404 error.

    :param area_connection_id: ID of the area connection to retrieve.
    :param area_connection_service: Service to handle the query and retrieve the connection.
    :return: Area connection details.
    """
    return await area_connection_service.get_area_connection_by_id(area_connection_id)


@router.put(
    "/{area_connection_id}",
    response_model=AreaConnectionResponseDTO,
    summary="Update existing area connection",
    responses={
        200: {
            "model": AreaConnectionResponseDTO,
            "description": "Connection updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Area connection not found"},
        409: {"model": ConflictError, "description": "Area connection conflict"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Update the details of an existing area connection by its ID.",
)
async def update_area_connection(
    area_connection_id: int,
    area_connection_request: AreaConnectionRequestDto,
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> AreaConnectionResponseDTO:
    """
    Endpoint to update an existing area connection.

    This endpoint allows updating the details of an existing connection identified by its ID. If the connection is updated successfully, it returns the updated data. If not found, it returns a 404 error.

    :param area_connection_id: ID of the connection to update.
    :param area_connection_request: New data for the area connection.
    :param area_connection_service: Service to handle the update logic.
    :return: Updated data of the area connection.
    """
    return await area_connection_service.update_area_connection(
        area_connection_id, area_connection_request
    )


@router.delete(
    "/{area_connection_id}",
    response_model=MessageResponse,
    summary="Delete area connection by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Connection deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Area connection not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Delete a specific area connection from the system using its ID.",
)
async def delete_area_connection(
    area_connection_id: int,
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> MessageResponse:
    """
    Endpoint to delete an area connection.

    This endpoint allows deleting a specific connection identified by its ID. If deleted successfully, it returns a success message. If not found, it returns a 404 error.

    :param area_connection_id: ID of the connection to delete.
    :param area_connection_service: Service to handle the deletion logic.
    :return: Success message indicating the connection has been deleted.
    """
    return await area_connection_service.delete_area_connection(area_connection_id)


@router.get(
    "/origin/{area_origen_id}",
    response_model=list[AreaConnectionResponseDTO],
    summary="Get connections by origin area ID",
    responses={
        200: {
            "model": list[AreaConnectionResponseDTO],
            "description": "List of area connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Origin area not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieve a list of area connections filtered by the origin area ID.",
)
async def get_connections_by_area_origen_id(
    area_origen_id: int,
    area_connection_service: IAreaConnectionService = Depends(
        get_area_connection_service
    ),
) -> list[AreaConnectionResponseDTO]:
    """
    Endpoint to retrieve area connections by origin area ID.

    This endpoint returns a list of all connections with the specified origin area. If no connections are found or if the origin area does not exist, appropriate errors are returned.

    :param area_origen_id: ID of the origin area to filter the connections.
    :param area_connection_service: Service to handle the query and retrieve filtered connections.
    :return: List of area connections with the specified origin area ID.
    """
    return await area_connection_service.get_connections_by_area_origen_id(
        area_origen_id
    )
