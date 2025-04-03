from abc import ABC, abstractmethod
from src.app.dto.request import UserRequestDTO
from src.app.dto.response import UserResponseDTO, UserPage
from src.app.schema import MessageResponse


class IUserService(ABC):
    """
    Interface for user service operations.
    Defines the contract for user-related business logic.
    """

    @abstractmethod
    async def add_user(self, user_request: UserRequestDTO) -> UserResponseDTO:
        """
        Add a new user.

        Args:
            user_request: The data transfer object containing user details.

        Returns:
            The created user as a UserResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_users(self) -> list[UserResponseDTO]:
        """
        Retrieve all users.

        Returns:
            A list of UserResponseDTO objects representing all users.
        """
        pass

    @abstractmethod
    async def update_user(
        self, user_id: int, user_request: UserRequestDTO
    ) -> UserResponseDTO:
        """
        Update an existing user.

        Args:
            user_id: The ID of the user to update.
            user_request: The data transfer object containing updated user details.

        Returns:
            The updated user as a UserResponseDTO.
        """
        pass

    @abstractmethod
    async def update_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> MessageResponse:
        """
        Update the password for a user.

        Args:
            user_id: The ID of the user whose password is to be updated.
            old_password: The current password of the user.
            new_password: The new password to set.

        Returns:
            A MessageResponse indicating the result of the update.
        """
        pass

    @abstractmethod
    async def update_user_status(self, user_id: int, status: str) -> MessageResponse:
        """
        Update the status of a user.

        Args:
            user_id: The ID of the user whose status is to be updated.
            status: The new status to set for the user.

        Returns:
            A MessageResponse indicating the result of the update.
        """
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> MessageResponse:
        """
        Delete a user by their ID.

        Args:
            user_id: The ID of the user to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserResponseDTO:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The user as a UserResponseDTO.
        """
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserResponseDTO:
        """
        Retrieve a user by their username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            The user as a UserResponseDTO.
        """
        pass

    @abstractmethod
    async def get_users_paginated(self, page: int, size: int) -> UserPage:
        """
        Retrieve a paginated list of users.

        Args:
            page: The page number to retrieve.
            size: The number of users per page.

        Returns:
            A UserPage object containing the paginated users.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> UserPage:
        """
        Find users based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of users per page.
            search_term: The term to search for in usernames.

        Returns:
            A UserPage object containing the users that match the search criteria.
        """
        pass
