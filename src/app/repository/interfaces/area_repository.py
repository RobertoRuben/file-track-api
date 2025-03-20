from abc import ABC, abstractmethod
from src.app.model.entity import Area
from src.app.schema import Page

class IAreaRepository(ABC):
    """
    Interface for the Area repository.
    """

    @abstractmethod
    async def save(self, area: Area) -> Area:
        """
        Save an area.

        Args:
            area: The area to save

        Returns:
            The saved area with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Area]:
        """
        Get all areas.

        Returns:
            A list containing all areas
        """
        pass

    @abstractmethod
    async def delete(self, area_id: int) -> bool:
        """
        Delete an area by its ID.

        Args:
            area_id: The ID of the area to delete

        Returns:
            True if the area was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, area_id: int) -> Area:
        """
        Get an area by its ID.

        Args:
            area_id: The ID of the area to retrieve

        Returns:
            The found area
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Get a paginated list of areas.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing areas and pagination information
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
        Find areas by search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with areas matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if an area exists based on the given criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching area exists, False otherwise
        """
        pass