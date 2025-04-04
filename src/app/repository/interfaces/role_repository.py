from abc import ABC, abstractmethod
from src.app.schema import Page
from src.app.model.entity import Role


class IRoleRepository(ABC):

    @abstractmethod
    async def save(self, rol: Role) -> Role:
        """
        Save a role entity to the database.

        :param rol: The role entity to save
        :return: The saved role with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Role]:
        """
        Retrieve all role entities from the database.

        :return: A list containing all roles
        """
        pass

    @abstractmethod
    async def delete(self, rol_id: int) -> bool:
        """
        Delete a role entity from the database by its ID.

        :param rol_id: The ID of the role to delete
        :return: True if the role was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, rol_id: int) -> Role:
        """
        Retrieve a role entity from the database by its ID.

        :param rol_id: The ID of the role to retrieve
        :return: The found role entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of role entities from the database.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing roles and pagination information
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

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with roles matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a role entity exists in the database based on specific criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching role exists, False otherwise
        """
        pass
