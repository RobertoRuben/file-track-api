from fastapi import APIRouter, Depends, Query
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.dto.request import RoleRequestDTO
from src.app.dto.response import RoleResponseDTO, RolePage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IRoleService
from src.app.service.dependencies import get_role_service

router = APIRouter(prefix="/role", tags=["Roles"])

role_tags_metadata = {
    "name": "Roles",
    "description": "Manages user roles within the system. "
    "These roles define permissions and access levels for system users. "
    "Allows complete CRUD operations, advanced search, and paginated listing.",
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
        409: {"model": ConflictError, "description": "Role already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new role in the system. The name must be unique.",
)
async def create_role(
    role_request: RoleRequestDTO,
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to create a new role.

    This endpoint allows the creation of a new role in the system. The role data
    must be provided in the request body. If the role is created successfully, a
    status code 201 is returned with the details of the created role.

    :param role_request: Request body containing the role data
    :param role_service: Service that handles the role creation logic
    :return: The data of the created role
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
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete list of all roles registered in the system, including their identifiers, names, and timestamps.",
)
async def get_all_roles(
    role_service: IRoleService = Depends(get_role_service),
) -> list[RoleResponseDTO]:
    """
    Endpoint to retrieve all roles.

    This endpoint returns a list of all available roles in the system. The response will include
    all roles stored in the database.

    :param role_service: Service to handle the query and retrieve all roles
    :return: A list of roles in the system
    """
    return await role_service.get_all_roles()


@router.get(
    "/paginated",
    response_model=RolePage,
    summary="Get roles with pagination",
    responses={
        200: {"model": RolePage, "description": "Paginated list of roles"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves roles in a paginated format to manage large data sets, allowing navigation through pages and control over the number of records per page.",
)
async def get_paginated_roles(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of roles per page"),
    role_service: IRoleService = Depends(get_role_service),
) -> RolePage:
    """
    Endpoint to retrieve roles in a paginated manner.

    This endpoint allows retrieving roles in a paginated format. The user can specify the page number
    and the number of roles per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve
    :param size: The number of roles to return per page
    :param role_service: Service to handle the query and return paginated roles
    :return: A paginated list of roles
    """
    return await role_service.get_paginated_roles(page, size)


@router.get(
    "/search",
    response_model=RolePage,
    summary="Search roles by term",
    responses={
        200: {"model": RolePage, "description": "Paginated list of roles"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs role searches based on a keyword or phrase. Results are returned paginated for better management of search results.",
)
async def find_roles(
    search_term: str | None = Query(None, description="Search term to filter roles"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of roles per page"),
    role_service: IRoleService = Depends(get_role_service),
) -> RolePage:
    """
    Endpoint to search roles using a search term.

    This endpoint allows searching for roles based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within role names
    :param page: The page number to retrieve
    :param size: The number of results per page
    :param role_service: Service to handle the search logic and return results
    :return: A paginated list of roles that match the search term
    """
    return await role_service.find(page, size, search_term)


@router.get(
    "/{role_id}",
    response_model=RoleResponseDTO,
    summary="Get role by ID",
    responses={
        200: {"model": RoleResponseDTO, "description": "Role found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves the complete details of a specific role using its unique identifier.",
)
async def get_role_by_id(
    role_id: int,
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to retrieve a role by its ID.

    This endpoint retrieves the details of a specific role identified by its ID. If the role is found,
    the role's data is returned. If not, a 404 error is returned.

    :param role_id: The ID of the role to retrieve
    :param role_service: Service to handle the query and retrieve the role
    :return:  details
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
        404: {"model": NotFoundError, "description": "Role not found"},
        409: {"model": ConflictError, "description": "Role name already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing role identified by its ID. Verifies that the new name is not already in use by another role.",
)
async def update_role(
    role_id: int,
    role_request: RoleRequestDTO,
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to update an existing role.

    This endpoint allows updating the details of an existing role identified by its ID. If the role
    is updated successfully, the updated role data is returned. If the role is not found,
    a 404 error is returned.

    :param role_id: The ID of the role to update
    :param role_request: The new data for the role
    :param role_service: Service to handle the update logic
    :return: The updated role data
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
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific role from the system using its ID. This operation is irreversible and may affect user associations.",
)
async def delete_role(
    role_id: int,
    role_service: IRoleService = Depends(get_role_service),
) -> MessageResponse:
    """
    Endpoint to delete a role.

    This endpoint allows deleting a specific role identified by its ID. If the role is deleted
    successfully, a success message is returned. If the role is not found, a 404 error is returned.

    :param role_id: The ID of the role to delete
    :param role_service: Service to handle the delete logic
    :return: A success message indicating that the role has been deleted
    """
    return await role_service.delete_role(role_id)
