from fastapi import APIRouter, Depends, Query, Security
from src.app.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
)
from src.app.model.enum import StatusEnum
from src.app.dto.request import UserRequestDTO
from src.app.dto.response import UserResponseDTO, CurrentUserResponseDTO, UserPage
from src.app.schema import MessageResponse
from src.app.service.interfaces import IUserService
from src.app.service.dependencies import (
    get_user_service,
    get_current_user,
)
from src.app.security.auth.constants import Scopes

router = APIRouter(prefix="/user", tags=["Users"])

user_tags_metadata = {
    "name": "Users",
    "description": "Manages users within the system. These operations allow creating, retrieving, "
    "updating, and deleting users, as well as searching and listing them with pagination.",
}


@router.post(
    "",
    response_model=UserResponseDTO,
    summary="Create a new user in the system",
    status_code=201,
    responses={
        201: {
            "model": UserResponseDTO,
            "description": "User created successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "Role or employee not found"},
        409: {"model": ConflictError, "description": "User already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Creates a new user in the system. Provide the user details in the request body to create it successfully.",
)
async def create_user(
    user_request: UserRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_CREATE]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to create a new user.

    This endpoint allows the creation of a new user in the system. The user data
    must be provided in the request body. If the user is created successfully, a status code 201
    with the created user's details is returned.

    :param user_request: Request body containing user data.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the user creation logic.
    :param _: Dependency to check if the user has the required scopes for this operation.
    :return: The created user data.
    """
    return await user_service.add_user(user_request)


@router.get(
    "",
    response_model=list[UserResponseDTO],
    summary="Get all users",
    responses={
        200: {
            "model": list[UserResponseDTO],
            "description": "List of users",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves a list of all users in the system.",
)
async def get_all_users(
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_READ]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> list[UserResponseDTO]:
    """
    Endpoint to retrieve all users.

    This endpoint returns a list of all available users in the system. The response will include
    all users stored in the database.

    :param user_service: Service to handle the query and retrieve all users.
    :param current_user: The user making the request, used for scope validation.
    :return: A list of users in the system.
    """
    return await user_service.get_all_users()


@router.get(
    "/paginated",
    response_model=UserPage,
    summary="Get users with pagination",
    responses={
        200: {"model": UserPage, "description": "Paginated list of users"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves users in a paginated format to manage large data sets.",
)
async def get_paginated_users(
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of users per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_READ]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> UserPage:
    """
    Endpoint to retrieve users in a paginated manner.

    This endpoint allows retrieving users in a paginated format. The user can specify the page number
    and the number of users per page to optimize the query and reduce data overload.

    :param page: The page number to retrieve.
    :param size: The number of users to return per page.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the query and return paginated users.
    :return: A paginated list of users.
    """
    return await user_service.get_users_paginated(page, size)


@router.get(
    "/search",
    response_model=UserPage,
    summary="Search users based on a term",
    responses={
        200: {"model": UserPage, "description": "Paginated list of users"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Search users based on a keyword or phrase, with pagination for better management of search results.",
)
async def find_users(
    search_term: str | None = Query(None, description="Search term to filter users"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of users per page"),
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_READ]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> UserPage:
    """
    Endpoint to search users using a search term.

    This endpoint allows searching for users based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param search_term: A term to search within usernames, role names, or employee names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the search logic and return results.
    :return: A paginated list of users that match the search term.
    """
    return await user_service.find(page, size, search_term)


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Get a specific user by ID",
    responses={
        200: {"model": UserResponseDTO, "description": "User found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific user using their ID.",
)
async def get_user_by_id(
    user_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_READ]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to retrieve a user by their ID.

    This endpoint retrieves the details of a specific user identified by their ID. If the user is found,
    the user's data is returned. If not, a 404 error is returned.

    :param user_id: The ID of the user to retrieve.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the query and retrieve the user.
    :return: The user details.
    """
    return await user_service.get_user_by_id(user_id)


@router.get(
    "/username/{username}",
    response_model=UserResponseDTO,
    summary="Get a specific user by username",
    responses={
        200: {"model": UserResponseDTO, "description": "User found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieve details of a specific user using their username.",
)
async def get_user_by_username(
    username: str,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_READ]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to retrieve a user by their username.

    This endpoint retrieves the details of a specific user identified by their username. If the user is found,
    the user's data is returned. If not, a 404 error is returned.

    :param username: The username of the user to retrieve.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the query and retrieve the user.
    :return: The user details.
    """
    return await user_service.get_user_by_username(username)


@router.put(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Update an existing user by ID",
    responses={
        200: {"model": UserResponseDTO, "description": "User updated successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {
            "model": NotFoundError,
            "description": "User, role, or employee not found",
        },
        409: {"model": ConflictError, "description": "Username already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the details of an existing user by their ID.",
)
async def update_user(
    user_id: int,
    user_request: UserRequestDTO,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_UPDATE]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to update an existing user.

    This endpoint allows updating the details of an existing user identified by their ID. If the user
    is updated successfully, the updated user data is returned. If the user is not found,
    a 404 error is returned.

    :param user_id: The ID of the user to update.
    :param user_request: The new data for the user.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the update logic.
    :return: The updated user data.
    """
    return await user_service.update_user(user_id, user_request)


@router.patch(
    "/{user_id}/password",
    response_model=MessageResponse,
    summary="Update user's password",
    responses={
        200: {"model": MessageResponse, "description": "Password updated successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the password for a specific user.",
)
async def update_password(
    user_id: int,
    old_password: str,
    new_password: str,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_UPDATE]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> MessageResponse:
    """
    Endpoint to update a user's password.

    This endpoint allows updating the password of a specific user identified by their ID.
    The old password must be provided for verification purposes.

    :param user_id: The ID of the user whose password is to be updated.
    :param old_password: The current password of the user.
    :param new_password: The new password to set.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the password update logic.
    :return: A message indicating the result of the password update.
    """
    return await user_service.update_password(user_id, old_password, new_password)


@router.patch(
    "/{user_id}/status",
    response_model=MessageResponse,
    summary="Update user's status",
    responses={
        200: {"model": MessageResponse, "description": "Status updated successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Updates the status (active/inactive) of a specific user.",
)
async def update_user_status(
    user_id: int,
    status: StatusEnum,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_UPDATE]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> MessageResponse:
    """
    Endpoint to update a user's status.

    This endpoint allows updating the status (active or inactive) of a specific user identified by their ID.

    :param user_id: The ID of the user whose status is to be updated.
    :param status: The new status to set for the user ("Activate" or "Deactivate").
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the status update logic.
    :return: A message indicating the result of the status update.
    """
    return await user_service.update_user_status(user_id, status)


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Delete a user by ID",
    responses={
        200: {"model": MessageResponse, "description": "User deleted successfully"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Deletes a specific user from the system using their ID.",
)
async def delete_user(
    user_id: int,
    current_user: CurrentUserResponseDTO = Security(
        get_current_user, scopes=[Scopes.USER_DELETE]
    ),
    user_service: IUserService = Depends(get_user_service),
) -> MessageResponse:
    """
    Endpoint to delete a user.

    This endpoint allows deleting a specific user identified by their ID. If the user is deleted
    successfully, a success message is returned. If the user is not found, a 404 error is returned.

    :param user_id: The ID of the user to delete.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the delete logic.
    :return: A success message indicating that the user has been deleted.
    """
    return await user_service.delete_user(user_id)
