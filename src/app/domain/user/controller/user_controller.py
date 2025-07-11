from datetime import datetime
from fastapi import (
    APIRouter,
    Depends,
    Query,
    Security,
    Body,
    Request,
    Response
)
from src.app.core.exception.schema import (
    BackRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
)
from src.app.core.exception.decorator import controller_handle_exceptions
from src.app.core.security.auth.constants import Scopes
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dependencies import get_current_user
from src.app.core.schema import MessageResponse
from src.app.domain.user.enum import StatusEnum
from src.app.domain.user.dto.request import UserRequestDTO
from src.app.domain.user.dto.response import UserResponseDTO, UserPage
from src.app.domain.user.service.interface import IUserService
from src.app.domain.user.service.dependencies import get_user_service


router = APIRouter(prefix="/users", tags=["Users"])

user_tags_metadata = {
    "name": "Users",
    "description": "Comprehensive enterprise user account management system providing complete user lifecycle "
    "administration, authentication control, and access management for organizational security. Manages user "
    "registrations, credential management, role assignments, and access control supporting enterprise security "
    "frameworks, identity management, and administrative coordination. Facilitates secure user account operations, "
    "permission management, and organizational access control for effective enterprise user administration.",
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Role or employee not found"},
        409: {"model": ConflictError, "description": "User already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Establishes new enterprise user accounts with comprehensive authentication setup, role assignment, "
    "and security validation for organizational access management. Creates detailed user profiles with unique "
    "credential requirements, role-based permissions, and employee associations supporting enterprise security "
    "frameworks, identity management systems, and organizational access control requiring secure user account "
    "provisioning and administrative coordination workflows.",
)
@controller_handle_exceptions
async def create_user(
    request: Request,
    user_request: UserRequestDTO,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_CREATE]),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to create a new user.

    This endpoint allows the creation of a new user in the system. The user data
    must be provided in the request body. If the user is created successfully, a status code 201
    with the created user's details is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive enterprise user registry including all registered accounts with authentication "
    "details, role assignments, and administrative metadata for complete organizational user oversight. Provides "
    "enterprise-wide access to user profiles supporting identity management, security auditing, administrative "
    "coordination, and access control management requiring complete user information access and security "
    "compliance capabilities for organizational user administration.",
)
@controller_handle_exceptions
async def get_all_users(
    request: Request,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_READ]),
    user_service: IUserService = Depends(get_user_service),
) -> list[UserResponseDTO]:
    """
    Endpoint to retrieve all users.

    This endpoint returns a list of all available users in the system. The response will include
    all users stored in the database.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Provides optimized paginated access to enterprise user collections with advanced status filtering "
    "for efficient large-scale user management and enhanced organizational system performance. Implements "
    "server-side pagination with configurable page sizes and active/inactive status filtering to handle "
    "extensive user registries, reduce memory consumption, and improve administrative experience through "
    "controlled data loading and targeted user subset access.",
)
@controller_handle_exceptions
async def get_paginated_users(
    request: Request,
    page: int = Query(default=1, description="Page number to retrieve"),
    size: int = Query(default=10, description="Number of users per page"),
    only_active: bool = Query(
        default=True,
        description="If True, returns only active users; if False, returns only inactive users",
    ),
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_READ]),
    user_service: IUserService = Depends(get_user_service),
) -> UserPage:
    """
    Endpoint to retrieve users in a paginated manner with active status filtering.

    This endpoint allows retrieving users in a paginated format. The user can specify the page number,
    the number of users per page, and filter by active status:
    - only_active=True: returns only active users
    - only_active=False: returns only inactive users

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param page: The page number to retrieve.
    :param size: The number of users to return per page.
    :param only_active: If True, returns only active users; if False, returns only inactive users.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the query and return paginated users.
    :return: A paginated list of users.
    """
    return await user_service.get_users_paginated(page, size, only_active)


@router.get(
    "/search",
    response_model=UserPage,
    summary="Search users based on a term",
    responses={
        200: {"model": UserPage, "description": "Paginated list of users"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes intelligent user search operations across authentication credentials, role assignments, "
    "and employee associations for precise user discovery within comprehensive enterprise systems. Implements "
    "secure search capabilities with paginated results across usernames, roles, and employee information while "
    "maintaining security compliance. Supports complex search scenarios including partial matches and case-"
    "insensitive queries for enhanced user identification and administrative efficiency.",
)
@controller_handle_exceptions
async def find_users(
    request: Request,
    search_term: str | None = Query(None, description="Search term to filter users"),
    page: int = Query(default=1, description="Page number for paginated results"),
    size: int = Query(default=10, description="Number of users per page"),
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_READ]),
    user_service: IUserService = Depends(get_user_service),
) -> UserPage:
    """
    Endpoint to search users using a search term.

    This endpoint allows searching for users based on a given search term. The results are returned
    in a paginated format, where the user can specify the page number and the number of results per page.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param search_term: A term to search within usernames, role names, or employee names.
    :param page: The page number to retrieve.
    :param size: The number of results per page.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the search logic and return results.
    :return: A paginated list of users that match the search term.
    """
    return await user_service.find(page, size, search_term)


@router.post(
    "/export-excel",
    response_class=Response,
    summary="Export users to Excel",
    responses={
        200: {
            "description": "Excel file with user data",
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            },
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "Users not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates comprehensive Excel reports containing detailed user information for specified accounts. "
    "Creates professionally formatted spreadsheets with complete user data including usernames, employee associations, "
    "role assignments, department information, and account status. Ideal for user management reporting, security auditing, "
    "administrative documentation, and external reporting requirements. Supports bulk export with optimized file generation "
    "for enterprise user administration and compliance reporting.",
)
@controller_handle_exceptions
async def export_users_to_excel(
    request: Request,
    user_ids: list[int] = Body(..., description="List of user IDs to export"),
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_READ]),
    user_service: IUserService = Depends(get_user_service),
) -> Response:
    """
    Generates comprehensive Excel reports for selected users.

    This endpoint creates professionally formatted Excel spreadsheets containing
    detailed user information for reporting, analysis, and compliance purposes.
    The generated files include complete user metadata, employee associations,
    role assignments, and formatting optimized for business use and external sharing.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param user_ids: List of unique identifiers for users to include in export
    :param current_user: Authenticated user with user export privileges
    :param user_service: Service layer handling Excel generation logic
    :return: Excel file as downloadable response with appropriate headers
    """
    excel_data = await user_service.export_users_to_excel(user_ids)

    current_datetime = datetime.now().strftime("%d%m%Y%H%M")
    filename = f"users_{current_datetime}.xlsx"

    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    return Response(content=excel_data, headers=headers)


@router.get(
    "/{user_id}",
    response_model=UserResponseDTO,
    summary="Get a specific user by ID",
    responses={
        200: {"model": UserResponseDTO, "description": "User found"},
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive user profile and authentication metadata for specific accounts using unique "
    "system identifiers. Provides complete user information including credential details, role assignments, "
    "employee associations, and security settings for detailed user analysis and organizational oversight. "
    "Essential for identity verification workflows, security auditing, and administrative processes requiring "
    "precise user identification and security-compliant data access.",
)
@controller_handle_exceptions
async def get_user_by_id(
    request: Request,
    user_id: int,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_READ]),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to retrieve a user by their ID.

    This endpoint retrieves the details of a specific user identified by their ID. If the user is found,
    the user's data is returned. If not, a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive user profile and authentication metadata for specific accounts using unique "
    "username identifiers. Provides complete user information including credential details, role assignments, "
    "employee associations, and security settings for detailed user analysis and organizational oversight. "
    "Essential for username-based identity verification workflows, security auditing, and administrative "
    "processes requiring precise user identification through username lookup.",
)
@controller_handle_exceptions
async def get_user_by_username(
    request: Request,
    username: str,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_READ]),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to retrieve a user by their username.

    This endpoint retrieves the details of a specific user identified by their username. If the user is found,
    the user's data is returned. If not, a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {
            "model": NotFoundError,
            "description": "User, role, or employee not found",
        },
        409: {"model": ConflictError, "description": "Username already exists"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs comprehensive user account modification including credential updates, role reassignments, "
    "and profile changes with security validation and organizational integrity preservation. Supports user "
    "lifecycle management workflows while maintaining authentication security, enforcing username uniqueness, "
    "and preserving role-based access control. Enables secure user account management through controlled "
    "modification workflows with change tracking for enterprise user administration and security compliance.",
)
@controller_handle_exceptions
async def update_user(
    request: Request,
    user_id: int,
    user_request: UserRequestDTO,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_UPDATE]),
    user_service: IUserService = Depends(get_user_service),
) -> UserResponseDTO:
    """
    Endpoint to update an existing user.

    This endpoint allows updating the details of an existing user identified by their ID. If the user
    is updated successfully, the updated user data is returned. If the user is not found,
    a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes secure password modification procedures with comprehensive authentication verification "
    "and credential validation for enhanced enterprise user security management. Implements password change "
    "workflows requiring current password verification, enforcing security policies, and maintaining "
    "authentication integrity. Provides secure credential management supporting identity protection, "
    "security compliance requirements, and organizational password policies for robust user account security.",
)
@controller_handle_exceptions
async def update_password(
    request: Request,
    user_id: int,
    old_password: str,
    new_password: str,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_UPDATE]),
    user_service: IUserService = Depends(get_user_service),
) -> MessageResponse:
    """
    Endpoint to update a user's password.

    This endpoint allows updating the password of a specific user identified by their ID.
    The old password must be provided for verification purposes.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Performs controlled user account status management enabling account activation and deactivation "
    "for organizational access control and security administration. Implements secure status modification "
    "workflows supporting user lifecycle management, temporary access restrictions, and administrative "
    "control over user privileges. Essential for maintaining organizational security through controlled "
    "user access management and enterprise-level account status governance for security compliance.",
)
@controller_handle_exceptions
async def update_user_status(
    request: Request,
    user_id: int,
    status: StatusEnum,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_UPDATE]),
    user_service: IUserService = Depends(get_user_service),
) -> MessageResponse:
    """
    Endpoint to update a user's status.

    This endpoint allows updating the status (active or inactive) of a specific user identified by their ID.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
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
        401: {"model": UnauthorizedError, "description": "Unauthorized access"},
        403: {"model": ForbiddenError, "description": "Forbidden access"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Executes secure user account removal operations with comprehensive data integrity validation "
    "and organizational impact assessment for permanent user account elimination. Implements controlled "
    "deletion procedures ensuring proper cleanup of associated authentication credentials, role assignments, "
    "and system references. Critical operation requiring careful consideration of data dependencies and "
    "organizational relationships before permanent user account deletion and security audit trail maintenance.",
)
@controller_handle_exceptions
async def delete_user(
    request: Request,
    user_id: int,
    current_user: CurrentUser = Security(get_current_user, scopes=[Scopes.USER_DELETE]),
    user_service: IUserService = Depends(get_user_service),
) -> MessageResponse:
    """
    Endpoint to delete a user.

    This endpoint allows deleting a specific user identified by their ID. If the user is deleted
    successfully, a success message is returned. If the user is not found, a 404 error is returned.

    :param request: FastAPI Request object,use to extract the controller route path where the exception occurred.
    :param user_id: The ID of the user to delete.
    :param current_user: The user making the request, used for scope validation.
    :param user_service: Service to handle the delete logic.
    :return: A success message indicating that the user has been deleted.
    """
    return await user_service.delete_user(user_id)
