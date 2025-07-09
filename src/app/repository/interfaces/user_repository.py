from abc import ABC, abstractmethod
from typing import Any

from src.app.core.schema import Page
from src.app.model.entity import User


class IUserRepository(ABC):
    """
    Interface for the User repository.
    """

    @abstractmethod
    async def save(self, user: User) -> User:
        """
        Save a user entity to the database.

        Args:
            user: The user entity to save

        Returns:
            The saved user with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[User]:
        """
        Retrieve all user entities from the database.

        Returns:
            A list containing all users
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """
        Delete a user entity from the database by its ID.

        Args:
            user_id: The ID of the user to delete

        Returns:
            True if the user was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        """
        Retrieve a user entity from the database by its ID.

        Args:
            user_id: The ID of the user to retrieve

        Returns:
            The found user entity
        """
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        """
        Retrieve a user entity from the database by its username.

        Args:
            username: The username of the user to retrieve

        Returns:
            The found user entity
        """
        pass

    @abstractmethod
    async def get_current_user_by_name(self, username: str) -> dict[str, Any] | None:
        """
        Retrieve the current user based on the username.

        Args:
            username: The username of the user to retrieve

        Returns:
            A dictionary containing user information
        """
        pass

    @abstractmethod
    async def get_pageable(
        self, page: int, size: int, only_active: bool = True
    ) -> Page:
        """
        Retrieve a paginated list of user entities from the database.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            only_active: If True, returns only active users; if False, returns all users

        Returns:
            A Page object containing users and pagination information
        """
        pass

    @abstractmethod
    async def find(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Retrieve a paginated list of user entities based on search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with users matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a user entity exists in the database based on specific criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching user exists, False otherwise
        """
        pass

    @abstractmethod
    async def find_by_ids(self, user_ids: list[int]) -> list[User]:
        """
        Retrieve multiple user entities from the database by their IDs.

        Args:
            user_ids: List of user IDs to retrieve

        Returns:
            List of found user entities
        """
        pass
