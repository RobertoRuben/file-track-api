from abc import ABC, abstractmethod
from src.app.model.entity import Hamlet
from src.app.schema import Page


class IHamletRepository(ABC):
    """
    Interface for the Hamlet repository.
    Defines the contract for hamlet data access operations.
    """

    @abstractmethod
    async def save(self, hamlet: Hamlet) -> Hamlet:
        """
        Save a hamlet entity to the database.

        :param hamlet: The hamlet entity to save
        :return: The saved hamlet with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Hamlet]:
        """
        Retrieve all hamlet entities from the database.

        :return: A list containing all hamlets
        """
        pass

    @abstractmethod
    async def delete(self, hamlet_id: int) -> bool:
        """
        Delete a hamlet entity from the database by its ID.

        :param hamlet_id: The ID of the hamlet to delete
        :return: True if the hamlet was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, hamlet_id: int) -> Hamlet:
        """
        Retrieve a hamlet entity from the database by its ID.

        :param hamlet_id: The ID of the hamlet to retrieve
        :return: The found hamlet entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of hamlet entities from the database.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing hamlets and pagination information
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
        Retrieve a paginated list of hamlet entities based on search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with hamlets matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a hamlet entity exists in the database based on specific criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching hamlet exists, False otherwise
        """
        pass

    @abstractmethod
    async def delete_by_ids(self, hamlet_ids: list[int]) -> bool:
        """
        Delete multiple hamlet entities from the database by their IDs.

        :param hamlet_ids: List of hamlet IDs to delete
        :return: True if the hamlets were successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def find_by_ids(self, hamlet_ids: list[int]) -> list[Hamlet]:
        """
        Retrieve multiple hamlet entities from the database by their IDs.

        :param hamlet_ids: List of hamlet IDs to retrieve
        :return: List of found hamlet entities
        """
        pass
