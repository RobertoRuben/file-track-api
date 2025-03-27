from abc import ABC, abstractmethod
from src.app.model.entity import Caserio
from src.app.schema import Page


class IHamletRepository(ABC):
    """
    Interface for the Hamlet repository.
    """

    @abstractmethod
    async def save(self, caserio: Caserio) -> Caserio:
        """
        Save a hamlet entity to the database.

        Args:
            caserio: The hamlet entity to save

        Returns:
            The saved hamlet with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Caserio]:
        """
        Retrieve all hamlet entities from the database.

        Returns:
            A list containing all hamlets
        """
        pass

    @abstractmethod
    async def delete(self, caserio_id: int) -> bool:
        """
        Delete a hamlet entity from the database by its ID.

        Args:
            caserio_id: The ID of the hamlet to delete

        Returns:
            True if the hamlet was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, caserio_id: int) -> Caserio:
        """
        Retrieve a hamlet entity from the database by its ID.

        Args:
            caserio_id: The ID of the hamlet to retrieve

        Returns:
            The found hamlet entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of hamlet entities from the database.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing hamlets and pagination information
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

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with hamlets matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a hamlet entity exists in the database based on specific criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching hamlet exists, False otherwise
        """
        pass
