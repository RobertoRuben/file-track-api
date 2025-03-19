from abc import ABC, abstractmethod
from src.schema import Page
from src.model.entity import Rol

class IRolRepository(ABC):

    @abstractmethod
    async def save(self, rol: Rol) -> Rol:
        """
        Save a role entity to the database.

        Args:
            rol: The role entity to save

        Returns:
            The saved role with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Rol]:
        """
        Retrieve all role entities from the database.

        Returns:
            A list containing all roles
        """
        pass

    @abstractmethod
    async def delete(self, rol_id: int) -> bool:
        """
        Delete a role entity from the database by its ID.

        Args:
            rol_id: The ID of the role to delete

        Returns:
            True if the role was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, rol_id: int) -> Rol:
        """
        Retrieve a role entity from the database by its ID.

        Args:
            rol_id: The ID of the role to retrieve

        Returns:
            The found role entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of role entities from the database.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing roles and pagination information
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
        Retrieve a paginated list of role entities based on search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with roles matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a role entity exists in the database based on specific criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching role exists, False otherwise
        """
        pass