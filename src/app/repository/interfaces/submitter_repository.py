from abc import ABC, abstractmethod
from src.app.model.entity import Submitter
from src.app.schema import Page


class ISubmitterRepository(ABC):
    """
    Interface for the Submitter repository.
    Defines the contract for data access operations related to submitters.
    """

    @abstractmethod
    async def save(self, submitter: Submitter) -> Submitter:
        """
        Save or update a submitter.

        :param submitter: The submitter entity to save
        :return: The saved submitter with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Submitter]:
        """
        Get all submitters.

        :return: A list containing all submitters
        """
        pass

    @abstractmethod
    async def delete(self, submitter_id: int) -> bool:
        """
        Delete a submitter by its ID.

        :param submitter_id: The ID of the submitter to delete
        :return: True if the submitter was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, submitter_id: int) -> Submitter:
        """
        Get a submitter by its ID.

        :param submitter_id: The ID of the submitter to retrieve
        :return: The found submitter
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Get a paginated list of submitters.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing submitters and pagination information
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
        Find submitters by search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with submitters matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a submitter exists based on the given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching submitter exists, False otherwise
        """
        pass
