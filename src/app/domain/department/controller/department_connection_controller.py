from fastapi import (
    APIRouter,
    Depends,
    Query,
    Security,
    Request
)
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    ForbiddenError,
    UnauthorizedError,
)
from src.app.core.exception.decorator import controller_handle_exceptions
from src.app.core.security.auth.constants import Scopes
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dependencies import get_current_user
from src.app.core.schema import MessageResponse
from src.app.domain.department.dto.request import DepartmentConnectionRequestDTO
from src.app.domain.department.dto.response import (
    DepartmentConnectionResponseDTO,
    DepartmentConnectionPage,
)
from src.app.domain.department.service.dependencies import (
    get_department_connection_service,
)
from src.app.domain.department.service.interface import IDepartmentConnectionService

router = APIRouter(prefix="/department-connections", tags=["Department Connections"])

department_connection_tags_metadata = {
    "name": "Department Connections",
    "description": "Comprehensive management of interdepartmental relationships and organizational network structures "
    "within the enterprise ecosystem. Handles the complex web of departmental connections including hierarchical "
    "reporting structures, workflow dependencies, communication channels, and functional relationships. Provides "
    "advanced CRUD operations, intelligent search capabilities, contextual filtering, and scalable pagination "
    "for efficient organizational structure visualization, strategic planning, and enterprise architecture analysis.",
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
    description="Establishes new organizational relationships between departments with comprehensive validation and "
    "hierarchical integrity checks. Creates bidirectional connections that define reporting structures, "
    "workflow dependencies, and communication pathways essential for organizational chart visualization "
    "and departmental coordination within the enterprise structure.",
)
@controller_handle_exceptions
async def create_department_connection(
    request: Request,
    department_connection: DepartmentConnectionRequestDTO,
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
    description="Retrieves the complete organizational network of all departmental relationships and connections "
    "within the enterprise structure. Provides comprehensive mapping of interdepartmental workflows, "
    "reporting hierarchies, and communication channels essential for organizational analysis, structure "
    "visualization, and strategic planning initiatives across the entire organizational ecosystem.",
)
@controller_handle_exceptions
async def get_all_department_connections(
    request: Request,
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
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
    description="Retrieves contextual departmental connections filtered by the authenticated user's organizational "
    "assignment, providing personalized access to relevant interdepartmental relationships. Ensures users "
    "only access connections pertinent to their departmental scope for enhanced security and operational "
    "focus within their specific organizational context and workflow requirements.",
)
@controller_handle_exceptions
async def get_connections_by_current_user_department_id(
    request: Request,
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
    description="Provides efficient paginated access to departmental connection networks for scalable organizational "
    "data management. Optimizes performance when handling extensive enterprise structures with numerous "
    "interdepartmental relationships, enabling systematic navigation through large connection datasets "
    "while maintaining responsive user experience and system performance.",
)
@controller_handle_exceptions
async def get_paginated_department_connections(
    request: Request,
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of connections per page"),
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
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
    description="Performs intelligent search across departmental connection networks using advanced matching algorithms "
    "for precise relationship discovery. Enables organizational analysis and structure exploration with "
    "flexible query capabilities, supporting department name searches, connection type filtering, and "
    "hierarchical relationship identification for comprehensive organizational insights.",
)
@controller_handle_exceptions
async def find_department_connections(
    request: Request,
    search_term: str | None = Query(
        None, description="Search term to filter connections"
    ),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of connections per page"),
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
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
    description="Retrieves comprehensive details of a specific departmental relationship using its unique organizational "
    "identifier. Provides complete connection information including source and target departments, relationship "
    "types, and hierarchical context essential for detailed organizational analysis and structure verification "
    "within the enterprise network.",
)
@controller_handle_exceptions
async def get_department_connection_by_id(
    request: Request,
    department_connection_id: int,
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
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
    description="Updates comprehensive departmental relationship configurations with validation of organizational "
    "hierarchy integrity and conflict prevention. Modifies existing connections while maintaining structural "
    "consistency, preventing circular dependencies, and ensuring valid organizational workflows within "
    "the enterprise architecture for seamless departmental coordination.",
)
@controller_handle_exceptions
async def update_department_connection(
    request: Request,
    department_connection_id: int,
    department_connection_request: DepartmentConnectionRequestDTO,
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
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
    description="Permanently removes a specific departmental relationship from the organizational structure with "
    "comprehensive impact analysis and cleanup procedures. This irreversible operation eliminates connections "
    "while maintaining referential integrity, updating organizational charts, and preserving audit trails "
    "for compliance and structural change documentation within the enterprise network.",
)
@controller_handle_exceptions
async def delete_department_connection(
    request: Request,
    department_connection_id: int,
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
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
    description="Retrieves comprehensive departmental relationship networks filtered by specific source department "
    "identification, providing detailed mapping of outbound organizational connections. Enables analysis "
    "of departmental influence, reporting structures, and downstream workflow dependencies essential for "
    "hierarchical planning and organizational impact assessment within the enterprise structure.",
)
@controller_handle_exceptions
async def get_connections_by_source_department_id(
    request: Request,
    source_department_id: int,
    current_user: CurrentUser = Security(
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

    :param request: FastAPI Request object, used to extract the controller route path where the exception occurred.
    :param source_department_id: ID of the source department to filter the connections.
    :param current_user: The user making the request, used for authorization.
    :param department_connection_service: Service to handle the query and retrieve filtered connections.
    :return: List of department connections with the specified source department ID.
    """
    return await department_connection_service.get_connections_by_source_department_id(
        source_department_id
    )
