from abc import ABC, abstractmethod
from src.app.core.schema import MessageResponse
from src.app.domain.user.dto.request import UserRequestDTO
from src.app.domain.user.dto.response import UserResponseDTO, UserPage


class IUserService(ABC):
    """
    Interface for user service operations.
    Defines the contract for user-related business logic.
    """

    @abstractmethod
    async def add_user(self, user_request: UserRequestDTO) -> UserResponseDTO:
        """
        Add a new user.

        :param user_request: The data transfer object containing user details
        :return: The created user as a UserResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_users(self) -> list[UserResponseDTO]:
        """
        Retrieve all users.

        :return: A list of UserResponseDTO objects representing all users
        """
        pass

    @abstractmethod
    async def update_user(
        self, user_id: int, user_request: UserRequestDTO
    ) -> UserResponseDTO:
        """
        Update an existing user.

        :param user_id: The ID of the user to update
        :param user_request: The data transfer object containing updated user details
        :return: The updated user as a UserResponseDTO
        """
        pass

    @abstractmethod
    async def update_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> MessageResponse:
        """
        Update the password for a user.

        :param user_id: The ID of the user whose password is to be updated
        :param old_password: The current password of the user
        :param new_password: The new password to set
        :return: A MessageResponse indicating the result of the update
        """
        pass

    @abstractmethod
    async def update_user_status(self, user_id: int, status: str) -> MessageResponse:
        """
        Update the status of a user.

        :param user_id: The ID of the user whose status is to be updated
        :param status: The new status to set for the user
        :return: A MessageResponse indicating the result of the update
        """
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> MessageResponse:
        """
        Delete a user by their ID.

        :param user_id: The ID of the user to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserResponseDTO:
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to retrieve
        :return: The user as a UserResponseDTO
        """
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserResponseDTO:
        """
        Retrieve a user by their username.

        :param username: The username of the user to retrieve
        :return: The user as a UserResponseDTO
        """
        pass

    @abstractmethod
    async def get_users_paginated(
        self, page: int, size: int, only_active: bool = True
    ) -> UserPage:
        """
        Retrieve a paginated list of users.

        :param page: The page number to retrieve
        :param size: The number of users per page
        :param only_active: If True, returns only active users; if False, returns all users
        :return: A UserPage object containing the paginated users
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> UserPage:
        """
        Find users based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of users per page
        :param search_term: The term to search for in usernames
        :return: A UserPage object containing the users that match the search criteria
        """
        pass

    @abstractmethod
    async def export_users_to_excel(self, user_ids: list[int]) -> bytes:
        """
        Export users to Excel format by their IDs.

        :param user_ids: List of user IDs to export
        :return: Excel file as bytes
        """
        pass
