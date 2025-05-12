from datetime import datetime
from src.app.model.entity import User
from src.app.model.enum import StatusEnum
from src.app.dto.request import UserRequestDTO
from src.app.dto.response import UserPage, UserResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import (
    IUserRepository,
    IRoleRepository,
    IEmployeeRepository,
)
from src.app.service.interfaces import IUserService
from src.app.security.hasher.interface import IHasherProvider


class UserServiceImpl(IUserService):
    """
    Implementation of the IUserService interface for managing user-related operations.

    :ivar user_repository: Repository to manage user data
    :ivar role_repository: Repository to manage role data
    :ivar employee_repository: Repository to manage employee data
    :ivar hasher_provider: Provider for password hashing operations
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        role_repository: IRoleRepository,
        employee_repository: IEmployeeRepository,
        hasher_provider: IHasherProvider,
    ):
        """
        Initialize the user service with required repositories and providers.

        :param user_repository: Repository for user data operations
        :param role_repository: Repository for role data operations
        :param employee_repository: Repository for employee data operations
        :param hasher_provider: Provider for password hashing operations
        """
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.employee_repository = employee_repository
        self.hasher_provider = hasher_provider

    @handle_exceptions
    async def add_user(self, user_request: UserRequestDTO) -> UserResponseDTO:
        """
        Adds a new user to the system.

        This method checks if the username, role, and employee are valid, and if the employee does not already have an associated user account.
        If all validations pass, a new user is created, and the password is hashed before being stored.

        :param user_request: DTO containing the details of the user to be added
        :return: DTO with the details of the newly created user
        :raises ConflictException: If the username already exists or if the employee already has an account
        :raises NotFoundException: If the role or employee does not exist
        """
        existing_username = await self.user_repository.exists_by(
            username=user_request.username
        )
        if existing_username:
            raise ConflictException(
                details=f"Username {user_request.username} already exists",
            )

        existing_role = await self.role_repository.exists_by(id=user_request.role_id)
        if not existing_role:
            raise NotFoundException(
                details=f"Role with ID {user_request.role_id} not found",
            )

        existing_employee = await self.employee_repository.exists_by(
            id=user_request.employee_id
        )
        if not existing_employee:
            raise NotFoundException(
                details=f"Employee with ID {user_request.employee_id} not found",
            )

        employee_has_user = await self.user_repository.exists_by(
            employee_id=user_request.employee_id
        )
        if employee_has_user:
            raise ConflictException(
                details=f"Employee with ID {user_request.employee_id} already has a user account",
            )

        hashed_password = await self.hasher_provider.encrypt(user_request.password)

        new_user = User(
            username=user_request.username,
            password=hashed_password,
            role_id=user_request.role_id,
            employee_id=user_request.employee_id,
        )

        created_user = await self.user_repository.save(new_user)

        return UserResponseDTO(
            id=created_user.id,
            username=created_user.username,
            is_active=created_user.is_active,
            role_id=created_user.role_id,
            employee_id=created_user.employee_id,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
        )

    @handle_exceptions
    async def get_all_users(self) -> list[UserResponseDTO]:
        """
        Retrieves all users from the system.

        This method returns a list of all users with their details, including their username, role, employee ID, and creation/update timestamps.

        :return: A list of DTOs with the details of all users
        """
        users = await self.user_repository.get_all()
        return [
            UserResponseDTO(
                id=user.id,
                username=user.username,
                is_active=user.is_active,
                role_id=user.role_id,
                employee_id=user.employee_id,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]

    @handle_exceptions
    async def update_user(
        self, user_id: int, user_request: UserRequestDTO
    ) -> UserResponseDTO:
        """
        Updates an existing user.

        This method allows updating a user's details, including username, role, employee association, and password (if a new password is provided).
        If any provided username, role, or employee does not exist, or if the username already exists, an exception is raised.

        :param user_id: ID of the user to be updated
        :param user_request: DTO containing the updated user details
        :return: DTO with the updated user details
        :raises NotFoundException: If the user with the given ID does not exist, or if the role or employee does not exist
        :raises ConflictException: If the username already exists for another user
        """
        existing_user_id = await self.user_repository.exists_by(id=user_id)
        if not existing_user_id:
            raise NotFoundException(
                details=f"User with ID {user_id} not found",
            )

        user = await self.user_repository.get_by_id(user_id)

        if user.username != user_request.username:
            existing_username = await self.user_repository.exists_by(
                username=user_request.username
            )
            if existing_username:
                raise ConflictException(
                    details=f"Username {user_request.username} already exists",
                )

        existing_role = await self.role_repository.exists_by(id=user_request.role_id)
        if not existing_role:
            raise NotFoundException(
                details=f"Role with ID {user_request.role_id} not found",
            )

        existing_employee = await self.employee_repository.exists_by(
            id=user_request.employee_id
        )
        if not existing_employee:
            raise NotFoundException(
                details=f"Employee with ID {user_request.employee_id} not found",
            )

        if user_request.password:
            hashed_password = await self.hasher_provider.encrypt(user_request.password)
            user.password = hashed_password

        user.username = user_request.username
        user.role_id = user_request.role_id
        user.employee_id = user_request.employee_id
        user.updated_at = datetime.now()

        updated_user = await self.user_repository.save(user)

        return UserResponseDTO(
            id=updated_user.id,
            username=updated_user.username,
            is_active=updated_user.is_active,
            role_id=updated_user.role_id,
            employee_id=updated_user.employee_id,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )

    @handle_exceptions
    async def update_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> MessageResponse:
        """
        Updates the password for an existing user.

        This method verifies that the old password is correct and then updates it with the new password.
        If the old password does not match, an exception is raised.

        :param user_id: ID of the user whose password is to be updated
        :param old_password: The current password of the user
        :param new_password: The new password to update
        :return: A response message indicating the result of the password update
        :raises NotFoundException: If the user with the given ID does not exist
        :raises BadRequestException: If the old password does not match the current password
        """
        existing_user_id = await self.user_repository.exists_by(id=user_id)
        if not existing_user_id:
            raise NotFoundException(
                details=f"User with ID {user_id} not found",
            )

        user = await self.user_repository.get_by_id(user_id)

        is_old_password_valid = await self.hasher_provider.verify(
            old_password, user.password
        )
        if not is_old_password_valid:
            raise BadRequestException(
                details="Old password is incorrect",
            )

        hashed_new_password = await self.hasher_provider.encrypt(new_password)

        user.password = hashed_new_password
        user.updated_at = datetime.now()

        await self.user_repository.save(user)

        return MessageResponse(
            message="Password updated successfully.",
            success=True,
            details=f"Password for user with ID {user_id} updated successfully.",
            status_code=200,
        )

    @handle_exceptions
    async def update_user_status(self, user_id: int, status: str) -> MessageResponse:
        """
        Updates the status of an existing user.

        This method updates the 'is_active' field of a user based on the provided status.
        The status is converted from a string value (either "Activate" or "Deactivate") to a boolean value.
        If the status is invalid, a BadRequestException is raised.

        :param user_id: ID of the user whose status is to be updated
        :param status: The status to update the user to. Should be either "Activate" or "Deactivate"
        :return: A response message indicating the result of the status update
        :raises NotFoundException: If the user with the given ID does not exist
        :raises BadRequestException: If the provided status is not valid
        """
        existing_user_id = await self.user_repository.exists_by(id=user_id)
        if not existing_user_id:
            raise NotFoundException(
                details=f"User with ID {user_id} not found",
            )

        user = await self.user_repository.get_by_id(user_id)

        status_value = status
        if hasattr(status, 'value'):
            status_value = status.value

        if status_value == StatusEnum.ACTIVATE.value:
            if user.is_active:
                raise BadRequestException(
                    message="Redundant status update",
                    details=f"User with ID {user_id} is already active.",
                )
            user.is_active = True
        elif status_value == StatusEnum.DEACTIVATE.value:
            if not user.is_active:
                raise BadRequestException(
                    message="Redundant status update",
                    details=f"User with ID {user_id} is already inactive.",
                )
            user.is_active = False
        else:
            raise BadRequestException(
                message="Invalid status value",
                details=f"Invalid status value: {status}. Valid values are 'Activate' or 'Deactivate'.",
            )

        user.updated_at = datetime.now()

        await self.user_repository.save(user)

        return MessageResponse(
            message="User status updated successfully.",
            success=True,
            details=f"Status for user with ID {user_id} updated to {status}.",
            status_code=200,
        )

    @handle_exceptions
    async def delete_user(self, user_id: int) -> MessageResponse:
        """
        Deletes a user by their ID.

        This method checks if the user exists. If the user is found, the user is deleted from the database.
        If the deletion is successful, a success message is returned. Otherwise, a failure message is returned.

        :param user_id: The ID of the user to delete
        :return: A response message indicating the result of the deletion process
        :raises NotFoundException: If the user with the given ID does not exist
        """
        existing_user_id = await self.user_repository.exists_by(id=user_id)
        if not existing_user_id:
            raise NotFoundException(
                details=f"User with ID {user_id} not found",
            )
        response = await self.user_repository.delete(user_id)
        if response is True:
            return MessageResponse(
                message="User deleted successfully.",
                success=True,
                details=f"User with ID {user_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete user.",
                success=False,
                details=f"Failed to delete user with ID {user_id}.",
                status_code=500,
            )

    @handle_exceptions
    async def get_user_by_id(self, user_id: int) -> UserResponseDTO:
        """
        Retrieves a user by their ID.

        This method checks if the user exists. If the user is found, their details are returned in a DTO format.
        If the user does not exist, an exception is raised.

        :param user_id: The ID of the user to retrieve
        :return: A DTO containing the user's details
        :raises NotFoundException: If the user with the given ID does not exist
        """
        existing_user_id = await self.user_repository.exists_by(id=user_id)
        if not existing_user_id:
            raise NotFoundException(
                details=f"User with ID {user_id} not found",
            )
        user = await self.user_repository.get_by_id(user_id)
        return UserResponseDTO(
            id=user.id,
            username=user.username,
            is_active=user.is_active,
            role_id=user.role_id,
            employee_id=user.employee_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @handle_exceptions
    async def get_user_by_username(self, username: str) -> UserResponseDTO:
        """
        Retrieves a user by their username.

        This method checks if the user exists. If the user is found, their details are returned in a DTO format.
        If the user does not exist, an exception is raised.

        :param username: The username of the user to retrieve
        :return: A DTO containing the user's details
        :raises NotFoundException: If the user with the given username does not exist
        """
        existing_username = await self.user_repository.exists_by(username=username)
        if not existing_username:
            raise NotFoundException(
                details=f"Username {username} not found",
            )
        user = await self.user_repository.get_by_username(username)
        return UserResponseDTO(
            id=user.id,
            username=user.username,
            is_active=user.is_active,
            role_id=user.role_id,
            employee_id=user.employee_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @handle_exceptions
    async def get_users_paginated(
        self, page: int, size: int, only_active: bool = True
    ) -> UserPage:
        """
        Retrieves a paginated list of users with option to filter by active status.

        This method validates the provided page and size values. If they are valid, it retrieves a paginated result
        of users from the repository. If the page or size is invalid (less than 1), a BadRequestException is raised.

        :param page: The page number to retrieve
        :param size: The number of items per page
        :param only_active: If True, returns only active users; if False, returns all users
        :return: A paginated response containing the user data and metadata
        :raises BadRequestException: If the page number or size is less than 1
        """
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid size",
                details="Size must be greater than 0.",
            )

        page_result = await self.user_repository.get_pageable(page, size, only_active)
        user_response = [UserResponseDTO(**user_dict) for user_dict in page_result.data]

        return UserPage(
            data=user_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> UserPage:
        """
        Searches for users based on a search term, and returns a paginated list of users matching the criteria.

        This method validates the provided page and size values. If they are valid, it searches for users whose
        username, role name, or employee name matches the provided search term. If no users match the search criteria,
        a NotFoundException is raised. If the page or size is invalid (less than 1), a BadRequestException is raised.

        :param page: The page number to retrieve
        :param size: The number of items per page
        :param search_term: The search term to filter users by username, role name, or employee name
        :return: A paginated response containing the user data and metadata
        :raises BadRequestException: If the page number or size is less than 1
        :raises NotFoundException: If no users match the search criteria
        """
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )

        if size < 1:
            raise BadRequestException(
                message="Invalid size",
                details="Size must be greater than 0.",
            )

        search_dict = {
            "username": search_term,
            "role_name": search_term,
            "employee_name": search_term,
        }

        page_result = await self.user_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details="No users match the search criteria.",
            )

        user_response = [UserResponseDTO(**user_dict) for user_dict in page_result.data]

        return UserPage(
            data=user_response,
            meta=page_result.meta,
        )
