from datetime import datetime
from fastapi import APIRouter, Depends, Query, Security, Body, Response
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.core.schema import MessageResponse
from src.app.core.security.auth.constants import Scopes
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dependencies import get_current_user
from src.app.domain.user.dto.request import RoleRequestDTO
from src.app.domain.user.dto.response import RoleResponseDTO, RolePage
from src.app.domain.user.service.interface import IRoleService
from src.app.domain.user.service.dependencies import get_role_service


router = APIRouter(prefix="/roles", tags=["Roles"])

role_tags_metadata = {
    "name": "Roles",
    "description": "Comprehensive enterprise role-based access control system managing organizational permissions, "
    "security hierarchies, and access level definitions for secure user authentication and authorization. "
    "Facilitates granular permission management, administrative oversight, and security compliance through "
    "structured role assignments supporting enterprise security frameworks, identity management systems, "
    "and organizational access governance. Enables secure role lifecycle management with advanced search "
    "capabilities, bulk operations, and detailed audit trails for enterprise security administration.",
}


@router.post(
    "",
    response_model=RoleResponseDTO,
    summary="Create a new role",
    status_code=201,
    responses={
        201: {
            "model": RoleResponseDTO,
            "description": "Role created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        409: {"model": ConflictError, "description": "Role already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new role in the system with the specified name and permissions. "
    "The role name must be unique across the entire system. This endpoint validates "
    "the role data and ensures no duplicate names exist before creating the role. "
    "Requires appropriate permissions to perform this operation.",
)
async def create_role(
    role_request: RoleRequestDTO,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_CREATE]),
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to create a new role.

    This endpoint allows the creation of a new role in the system. The role data
    must be provided in the request body. If the role is created successfully, a
    status code 201 is returned with the details of the created role.

    :param role_request: Request body containing the role data.
    :param current_user: The user creating the role, used for authorization.
    :param role_service: Service that handles the role creation logic.
    :return: The data of the created role.
    """
    return await role_service.add_role(role_request)


@router.get(
    "",
    response_model=list[RoleResponseDTO],
    summary="Get all roles",
    responses={
        200: {
            "model": list[RoleResponseDTO],
            "description": "List of roles",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a comprehensive list of all roles currently registered in the system. "
    "This endpoint returns complete role information including identifiers, names, descriptions, "
    "creation timestamps, and last modification dates. The response includes all active roles "
    "without any filtering or pagination applied.",
)
async def get_all_roles(
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_READ]),
    role_service: IRoleService = Depends(get_role_service),
) -> list[RoleResponseDTO]:
    """
    Endpoint to retrieve all roles.

    This endpoint returns a list of all available roles in the system. The response will include
    all roles stored in the database.

    :param current_user: The user requesting the roles, used for authorization.
    :param role_service: Service to handle the query and retrieve all roles.
    :return: A list of roles in the system.
    """
    return await role_service.get_all_roles()


@router.get(
    "/paginated",
    response_model=RolePage,
    summary="Get roles with pagination",
    responses={
        200: {"model": RolePage, "description": "Paginated list of roles"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves roles using a paginated approach to efficiently handle large datasets. "
    "This endpoint allows clients to navigate through role collections by specifying page numbers "
    "and page sizes. The response includes metadata such as total records, total pages, current page, "
    "and navigation flags (hasNext, hasPrevious) to facilitate user interface pagination controls. "
    "Ideal for displaying role lists in data tables or grids with performance optimization.",
)
async def get_paginated_roles(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of roles per page"),
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_READ]),
    role_service: IRoleService = Depends(get_role_service),
) -> RolePage:
    """
    Endpoint to retrieve roles in a paginated manner.

    This endpoint allows retrieving roles in a paginated format. The user can specify the page number
    and the number of roles per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of roles to return per page.
    :param current_user: The user requesting the roles, used for authorization.
    :param role_service: Service to handle the query and return paginated roles.
    :return: A paginated list of roles.
    """
    return await role_service.get_paginated_roles(page, size)


@router.get(
    "/search",
    response_model=RolePage,
    summary="Search roles by term",
    responses={
        200: {"model": RolePage, "description": "Paginated list of roles"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs advanced role searches using flexible text matching against role names and descriptions. "
    "The search functionality supports partial text matching and case-insensitive queries to provide "
    "comprehensive search results. Results are returned in a paginated format with configurable page "
    "sizes to optimize performance and user experience. If no search term is provided, returns all roles "
    "in paginated format. This endpoint is ideal for implementing search bars and filtering capabilities "
    "in user interfaces.",
)
async def find_roles(
    search_term: str | None = Query(None, description="Search term to filter roles"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of roles per page"),
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_READ]),
    role_service: IRoleService = Depends(get_role_service),
) -> RolePage:
    """
    Endpoint to search roles using a search term.

    This endpoint allows searching for roles based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within role names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user requesting the search, used for authorization.
    :param role_service: Service to handle the search logic and return results.
    :return: A paginated list of roles that match the search term.
    """
    return await role_service.find(page, size, search_term)


@router.delete(
    "/bulk",
    response_model=MessageResponse,
    summary="Delete multiple roles",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Roles deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "One or more roles not found",
        },
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs bulk deletion of multiple roles in a single atomic operation using their unique identifiers. "
    "This endpoint accepts a list of role IDs and removes all corresponding roles from the system. "
    "The operation is transactional - either all specified roles are deleted successfully, or none are deleted "
    "if any error occurs. Before deletion, the system validates that all provided role IDs exist and that "
    "the user has sufficient permissions. This operation is irreversible and may impact user-role associations "
    "throughout the system. Use with caution in production environments.",
)
async def delete_roles_bulk(
    role_ids: list[int] = Body(..., description="List of role IDs to delete"),
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_DELETE]),
    role_service: IRoleService = Depends(get_role_service),
) -> MessageResponse:
    """
    Endpoint to delete multiple roles.

    This endpoint allows deleting multiple roles identified by their IDs. If all roles
    are deleted successfully, a success message is returned. If any role is not found, a 404 error
    is returned. The request body should contain a list of role IDs.

    :param role_ids: List of role IDs to delete.
    :param current_user: The user performing the operation, used for authorization.
    :param role_service: Service to handle the bulk delete logic.
    :return: A success message indicating that the roles have been deleted.
    """
    return await role_service.delete_roles_by_ids(role_ids)


@router.post(
    "/export-excel",
    response_class=Response,
    summary="Export roles to Excel",
    responses={
        200: {"description": "Excel file containing the requested roles"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "No roles found to export"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates and downloads an Excel spreadsheet containing detailed information about selected roles. "
    "This endpoint creates a professionally formatted Excel file with role data including names, descriptions, "
    "creation dates, and other relevant metadata. The exported file includes proper headers, formatting, and "
    "is optimized for reporting and data analysis purposes. The filename includes a timestamp to ensure "
    "uniqueness and traceability. This feature is particularly useful for administrative reporting, "
    "data backup, and sharing role information with external stakeholders.",
)
async def export_roles_to_excel(
    role_ids: list[int] = Body(..., description="List of role IDs to export"),
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_READ]),
    role_service: IRoleService = Depends(get_role_service),
) -> Response:
    """
    Endpoint to export selected roles to Excel.

    This endpoint exports the selected roles to an Excel file format.

    :param role_ids: List of IDs of roles to export
    :param current_user: The user performing the export, used for authorization
    :param role_service: Service to handle the export logic
    :return: Excel file as a downloadable response
    """
    excel_data = await role_service.export_roles_to_excel(role_ids)

    current_datetime = datetime.now().strftime("%d%m%Y%H%M")
    filename = f"{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    return Response(content=excel_data, headers=headers)


@router.get(
    "/{role_id}",
    response_model=RoleResponseDTO,
    summary="Get role by ID",
    responses={
        200: {"model": RoleResponseDTO, "description": "Role found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive details of a specific role using its unique identifier. "
    "This endpoint returns complete role information including the role's name, description, "
    "creation timestamp, last modification date, and any associated metadata. The role ID must "
    "be a valid integer corresponding to an existing role in the system. This endpoint is ideal "
    "for displaying detailed role information in user interfaces, role management dashboards, "
    "or when performing role-specific operations.",
)
async def get_role_by_id(
    role_id: int,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_READ]),
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to retrieve a role by its ID.

    This endpoint retrieves the details of a specific role identified by its ID. If the role is found,
    the role's data is returned. If not, a 404 error is returned.

    :param role_id: The ID of the role to retrieve.
    :param current_user: The user requesting the role, used for authorization.
    :param role_service: Service to handle the query and retrieve the role.
    :return:  details.
    """
    return await role_service.get_role_by_id(role_id)


@router.put(
    "/{role_id}",
    response_model=RoleResponseDTO,
    summary="Update existing role",
    responses={
        200: {
            "model": RoleResponseDTO,
            "description": "Role updated successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Role not found"},
        409: {"model": ConflictError, "description": "Role name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing role identified by its unique ID. This endpoint allows "
    "modification of role properties such as name and description while maintaining data integrity. "
    "The system validates that the new role name is unique across the entire system (excluding the "
    "current role being updated). All changes are validated before being persisted to ensure consistency. "
    "The operation updates the role's modification timestamp automatically. This endpoint is essential "
    "for role management and administrative maintenance tasks.",
)
async def update_role(
    role_id: int,
    role_request: RoleRequestDTO,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_UPDATE]),
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to update an existing role.

    This endpoint allows updating the details of an existing role identified by its ID. If the role
    is updated successfully, the updated role data is returned. If the role is not found,
    a 404 error is returned.

    :param role_id: The ID of the role to update.
    :param role_request: The new data for the role.
    :param current_user: The user updating the role, used for authorization.
    :param role_service: Service to handle the update logic.
    :return: The updated role data.
    """
    return await role_service.update_role(role_id, role_request)


@router.delete(
    "/{role_id}",
    response_model=MessageResponse,
    summary="Delete role",
    responses={
        200: {
            "model": MessageResponse,
            "description": "Role deleted successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Permanently removes a specific role from the system using its unique identifier. "
    "This operation is irreversible and will completely delete the role and all its associated "
    "metadata from the database. Before deletion, the system may check for existing associations "
    "with users or other entities to prevent data integrity issues. Any users currently assigned "
    "to this role may be affected by this operation. This endpoint should be used with extreme "
    "caution, particularly in production environments, and typically requires elevated privileges.",
)
async def delete_role(
    role_id: int,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.ROLE_DELETE]),
    role_service: IRoleService = Depends(get_role_service),
) -> MessageResponse:
    """
    Endpoint to delete a role.

    This endpoint allows deleting a specific role identified by its ID. If the role is deleted
    successfully, a success message is returned. If the role is not found, a 404 error is returned.

    :param role_id: The ID of the role to delete.
    :param current_user: The user deleting the role, used for authorization.
    :param role_service: Service to handle the delete logic.
    :return: A success message indicating that the role has been deleted.
    """
    return await role_service.delete_role(role_id)
