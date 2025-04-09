from fastapi import APIRouter, Depends, Query, Security
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    ForbiddenError,
    UnauthorizedError,
)
from src.app.dto.request import DepartmentConnectionRequestDTO
from src.app.dto.response import (
    DepartmentConnectionResponseDTO,
    DepartmentConnectionPage,
    CurrentUserResponseDTO,
)
from src.app.schema import MessageResponse
from src.app.service.dependencies import (
    get_department_connection_service,
    get_current_user,
)
from src.app.service.interfaces import IDepartmentConnectionService
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/department-connections", tags=["Department Connections"])

department_connection_tags_metadata = {
    "name": "Department Connections",
    "description": "Manages connections between organizational departments in the system. "
    "These connections represent the hierarchical and functional relationships "
    "between departments, allowing the visualization of organizational structure. "
    "Provides CRUD operations, advanced search capabilities, and pagination features.",
}


@router.post(
    "",
    response_model=DepartmentConnectionResponseDTO,
    summary="Create a new department connection",
    status_code=201,
    responses={
        201: {
            "model": DepartmentConnectionResponseDTO,
            "description": "Department connection created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {
            "model": ConflictError,
            "description": "Department connection already exists",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new connection between two departments in the organization, establishing a relationship "
    "between source and target departments.",
)
async def create_department_connection(
    department_connection: DepartmentConnectionRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_CREATE]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> DepartmentConnectionResponseDTO:
    """
    Endpoint to create a new department connection.

    This endpoint allows the creation of a new relationship between two departments in the system.
    The connection data must be provided in the request body. If the connection is created successfully,
    a status code 201 is returned with the details of the created connection.

    :param department_connection: Request body containing the department connection data.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service that handles the department connection creation logic.
    :return: The data of the created department connection.
    """
    return await department_connection_service.add_department_connection(
        department_connection
    )


@router.get(
    "",
    response_model=list[DepartmentConnectionResponseDTO],
    summary="Get all department connections",
    responses={
        200: {
            "model": list[DepartmentConnectionResponseDTO],
            "description": "List of department connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete list of all department connections registered in the system, including their "
    "source and target departments.",
)
async def get_all_department_connections(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_READ]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> list[DepartmentConnectionResponseDTO]:
    """
    Endpoint to retrieve all department connections.

    This endpoint returns a list of all available department connections in the system. The response will include
    all connections stored in the database.

    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the query and retrieve all department connections.
    :return: A list of department connections in the system.
    """
    return await department_connection_service.get_all_department_connections()


@router.get(
    "/current-department",
    response_model=list[DepartmentConnectionResponseDTO],
    summary="Get department connections list by current user",
    responses={
        200: {
            "model": list[DepartmentConnectionResponseDTO],
            "description": "List of department connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Source department not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieves all department connections linked to the authenticated user's department, ensuring that "
    "only connections relevant to the user's organizational context are returned.",
)
async def get_connections_by_current_user_department_id(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_READ]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> list[DepartmentConnectionResponseDTO]:
    """
    Endpoint to retrieve department connections for the current user's department.

    This endpoint fetches all department connections associated with the department
    of the currently authenticated user. It filters the connections based on the user's
    department affiliation and returns a list of department connection details.
    Appropriate error responses are provided for cases such as malformed requests,
    unauthorized access, or if the source department is not found.

    :param current_user: The currently authenticated user, providing the necessary department context.
    :param department_connection_service: Service responsible for retrieving the department connections linked to the
     user's department.
    :return: A list of DepartmentConnectionResponseDTO objects containing the department connections.
    """
    return await department_connection_service.get_department_connections_by_current_user_department(
        current_user
    )


@router.get(
    "/paginated",
    response_model=DepartmentConnectionPage,
    summary="Get department connections with pagination",
    responses={
        200: {
            "model": DepartmentConnectionPage,
            "description": "Paginated list of department connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves department connections in a paginated format to manage large datasets, allowing navigation "
    "through pages and control over the number of records per page.",
)
async def get_paginated_department_connections(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of connections per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_READ]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> DepartmentConnectionPage:
    """
    Endpoint to retrieve department connections in a paginated manner.

    This endpoint allows for retrieving department connections in a paginated format. The user can specify the page
    number and the number of connections per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of department connections to return per page.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the query and return paginated connections.
    :return: A paginated list of department connections.
    """
    return await department_connection_service.get_paginated_department_connections(
        page, size
    )


@router.get(
    "/search",
    response_model=DepartmentConnectionPage,
    summary="Search department connections by term",
    responses={
        200: {
            "model": DepartmentConnectionPage,
            "description": "Paginated list of connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Connection not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Performs department connection searches based on a keyword or phrase. Results are returned paginated "
    "for better management of search results.",
)
async def find_department_connections(
    search_term: str | None = Query(
        None, description="Search term to filter connections"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of connections per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_READ]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> DepartmentConnectionPage:
    """
    Endpoint to search department connections using a search term.

    This endpoint allows searching for department connections based on a given term. Results are returned in a
    paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: Term to search for in the department connection details.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the search logic and return the results.
    :return: A paginated list of department connections that match the search term.
    """
    return await department_connection_service.find(page, size, search_term)


@router.get(
    "/{department_connection_id}",
    response_model=DepartmentConnectionResponseDTO,
    summary="Get department connection by ID",
    responses={
        200: {
            "model": DepartmentConnectionResponseDTO,
            "description": "Department connection found",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Department connection not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieves the complete details of a specific department connection using its unique identifier.",
)
async def get_department_connection_by_id(
    department_connection_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_READ]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> DepartmentConnectionResponseDTO:
    """
    Endpoint to retrieve a department connection by its ID.

    This endpoint retrieves the details of a specific department connection identified by its ID.
    If found, it returns the connection data. If not, it returns a 404 error.

    :param department_connection_id: ID of the department connection to retrieve.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the query and retrieve the connection.
    :return: Department connection details.
    """
    return await department_connection_service.get_department_connection_by_id(
        department_connection_id
    )


@router.put(
    "/{department_connection_id}",
    response_model=DepartmentConnectionResponseDTO,
    summary="Update existing department connection",
    responses={
        200: {
            "model": DepartmentConnectionResponseDTO,
            "description": "Connection updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Department connection not found"},
        409: {"model": ConflictError, "description": "Department connection conflict"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Updates the details of an existing department connection identified by its ID, verifying that the new"
    " relationship does not conflict with existing connections.",
)
async def update_department_connection(
    department_connection_id: int,
    department_connection_request: DepartmentConnectionRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_UPDATE]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> DepartmentConnectionResponseDTO:
    """
    Endpoint to update an existing department connection.

    This endpoint allows updating the details of an existing connection identified by its ID.
    If the connection is updated successfully, it returns the updated data. If not found, it returns a 404 error.

    :param department_connection_id: ID of the connection to update.
    :param department_connection_request: New data for the department connection.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the update logic.
    :return: Updated data of the department connection.
    """
    return await department_connection_service.update_department_connection(
        department_connection_id, department_connection_request
    )


@router.delete(
    "/{department_connection_id}",
    response_model=MessageResponse,
    summary="Delete department connection by ID",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Connection deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Department connection not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Deletes a specific department connection from the system using its ID. This operation is irreversible"
    " and affects the organizational structure representation.",
)
async def delete_department_connection(
    department_connection_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_DELETE]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> MessageResponse:
    """
    Endpoint to delete a department connection.

    This endpoint allows deleting a specific connection identified by its ID. If deleted successfully,
    it returns a success message. If not found, it returns a 404 error.

    :param department_connection_id: ID of the connection to delete.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the deletion logic.
    :return: Success message indicating the connection has been deleted.
    """
    return await department_connection_service.delete_department_connection(
        department_connection_id
    )


@router.get(
    "/source/{source_department_id}",
    response_model=list[DepartmentConnectionResponseDTO],
    summary="Get connections by source department ID",
    responses={
        200: {
            "model": list[DepartmentConnectionResponseDTO],
            "description": "List of department connections",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Source department not found"},
        500: {
            "model": InternalServerError,
            "description": "Internal server error",
        },
    },
    description="Retrieves a list of department connections filtered by the source department ID, showing all "
    "relationships originating from a specific department.",
)
async def get_connections_by_source_department_id(
    source_department_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.DEPARTMENT_CONNECTION_READ]
    ),
    department_connection_service: IDepartmentConnectionService = Depends(
        get_department_connection_service
    ),
) -> list[DepartmentConnectionResponseDTO]:
    """
    Endpoint to retrieve department connections by source department ID.

    This endpoint returns a list of all connections with the specified source department.
    If no connections are found or if the source department does not exist, appropriate errors are returned.

    :param source_department_id: ID of the source department to filter the connections.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the query and retrieve filtered connections.
    :return: List of department connections with the specified source department ID.
    """
    return await department_connection_service.get_connections_by_source_department_id(
        source_department_id
    )
