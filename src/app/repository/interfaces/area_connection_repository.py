from abc import ABC, abstractmethod
from src.app.model.entity import ComunicacionArea
from src.app.schema import Page


class IAreaConnectionRepository(ABC):
    """
    Interface for the ComunicacionArea repository.
    """

    @abstractmethod
    async def save(self, comunicacion_area: ComunicacionArea) -> ComunicacionArea:
        """
        Saves a communication between areas.

        Args:
            comunicacion_area: The communication between areas to save

        Returns:
            The saved communication between areas with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[ComunicacionArea]:
        """
        Gets all communications between areas.

        Returns:
            A list with all communications between areas
        """
        pass

    @abstractmethod
    async def delete(self, comunicacion_area_id: int) -> bool:
        """
        Deletes a communication between areas by its ID.

        Args:
            comunicacion_area_id: The ID of the communication between areas to delete

        Returns:
            True if the communication was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, comunicacion_area_id: int) -> ComunicacionArea:
        """
        Gets a communication between areas by its ID.

        Args:
            comunicacion_area_id: The ID of the communication between areas to retrieve

        Returns:
            The found communication between areas
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Gets a paginated list of communications between areas.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing communications between areas and pagination information
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
        Searches for communications between areas according to search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with communications between areas that match the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if a communication between areas exists according to given criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching communication between areas exists, False otherwise
        """
        pass
