from fastapi import APIRouter, Depends, Query
from src.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError
)
from src.dto.request import RoleRequestDTO
from src.dto.response import RoleResponseDTO, RolePage
from src.schema import MessageResponse
from src.service.interfaces import IRoleService
from src.service.dependencies import get_role_service

router = APIRouter(
    prefix="/role",
    tags=["Role"]
)

role_tags_metadata = {
    "name": "Role",
    "description": "Manage roles within the system. These operations allow you to create, retrieve, update, and "
                   "delete roles, as well as search and list them with pagination.",
}

@router.post(
    "",
    response_model=RoleResponseDTO,
    summary="Create a new role in the system",
    status_code=201,
    responses={
        201: {"model": RoleResponseDTO, "description": "Role created successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        409: {"model": ConflictError, "description": "Role already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Create a new role in the system. Provide the role's details in the request body to successfully create it.",
)
async def create_role(
    role_request: RoleRequestDTO,
    role_service: IRoleService = Depends(get_role_service)
) -> RoleResponseDTO:
    """
    Endpoint to create a new role.

    This endpoint allows the creation of a new role in the system. The role's data
    should be provided in the request body. If the role is created successfully, a 201 status
    code is returned with the created role's information.

    :param role_request: The request body containing the role's data.
    :param role_service: Service to handle the role creation logic.
    :return: The created role's data.
    """
    return await role_service.add_role(role_request)


@router.get(
    "",
    response_model=list[RoleResponseDTO],
    summary="Retrieve all roles in the system",
    responses={
        200: {"model": list[RoleResponseDTO], "description": "List of roles"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve a list of all roles in the system.",
)
async def get_all_roles(
    role_service: IRoleService = Depends(get_role_service),
) -> list[RoleResponseDTO]:
    """
    Endpoint to retrieve all roles.

    This endpoint returns a list of all roles available in the system. The response will include
    all roles stored in the database.

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
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve roles in a paginated format to manage large datasets.",
)
async def get_paginated_roles(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of roles per page"),
    role_service: IRoleService = Depends(get_role_service),
) -> RolePage:
    """
    Endpoint to retrieve roles in a paginated manner.

    This endpoint allows for retrieving roles in a paginated format. The user can specify the page
    number and the number of roles per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of roles to return per page.
    :param role_service: Service to handle the query and return paginated roles.
    :return: A paginated list of roles.
    """
    return await role_service.get_paginated_roles(page, size)


@router.get(
    "/search",
    response_model=RolePage,
    summary="Search for roles based on a term",
    responses={
        200: {"model": RolePage, "description": "Paginated list of roles"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search roles based on a keyword or phrase, with pagination for better management of search results.",
)
async def find_roles(
    search_term: str | None = Query(None, description="Search term to filter roles"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of roles per page"),
    role_service: IRoleService = Depends(get_role_service),
) -> RolePage:
    """
    Endpoint to search for roles using a search term.

    This endpoint allows for searching roles based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search for within role names or descriptions.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param role_service: Service to handle the search logic and return the results.
    :return: A paginated list of roles matching the search term.
    """
    return await role_service.find(page, size, search_term)


@router.get(
    "/{role_id}",
    response_model=RoleResponseDTO,
    summary="Get a specific role by ID",
    responses={
        200: {"model": RoleResponseDTO, "description": "Role found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve the details of a specific role using its ID.",
)
async def get_role_by_id(
    role_id: int,
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to retrieve a role by its ID.

    This endpoint retrieves the details of a specific role identified by its ID. If the role is found,
    it returns the role's data. If not, a 404 error is returned.

    :param role_id: The ID of the role to retrieve.
    :param role_service: Service to handle the query and retrieve the role.
    :return: The role's details.
    """
    return await role_service.get_role_by_id(role_id)


@router.put(
    "/{role_id}",
    response_model=RoleResponseDTO,
    summary="Update an existing role by ID",
    responses={
        200: {"model": RoleResponseDTO, "description": "Role updated successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Update the details of an existing role by its ID.",
)
async def update_role(
    role_id: int,
    role_request: RoleRequestDTO,
    role_service: IRoleService = Depends(get_role_service),
) -> RoleResponseDTO:
    """
    Endpoint to update an existing role.

    This endpoint allows for updating the details of an existing role identified by its ID. If the role
    is updated successfully, the updated role data is returned. If the role is not found, a 404 error is returned.

    :param role_id: The ID of the role to update.
    :param role_request: The new data for the role.
    :param role_service: Service to handle the update logic.
    :return: The updated role's data.
    """
    return await role_service.update_role(role_id, role_request)


@router.delete(
    "/{role_id}",
    response_model=MessageResponse,
    summary="Delete a role by ID",
    responses={
        200: {"model": MessageResponse, "description": "Role deleted successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Role not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Delete a specific role from the system using its ID.",
)
async def delete_role(
    role_id: int,
    role_service: IRoleService = Depends(get_role_service),
) -> MessageResponse:
    """
    Endpoint to delete a role.

    This endpoint allows for deleting a specific role identified by its ID. If the role is successfully
    deleted, a success message is returned. If the role is not found, a 404 error is returned.

    :param role_id: The ID of the role to delete.
    :param role_service: Service to handle the deletion logic.
    :return: A success message indicating the role has been deleted.
    """
    return await role_service.delete_role(role_id)
