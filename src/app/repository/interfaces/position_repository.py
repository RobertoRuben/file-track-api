from abc import ABC, abstractmethod
from src.app.model.entity import Cargo
from src.app.schema import Page


class IPositionRepository(ABC):
    """
    Interface for the Cargo repository.
    """

    @abstractmethod
    async def save(self, cargo: Cargo) -> Cargo:
        """
        Save a position entity to the database.

        Args:
            cargo: The position entity to save

        Returns:
            The saved position with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Cargo]:
        """
        Retrieve all position entities from the database.

        Returns:
            A list containing all positions
        """
        pass

    @abstractmethod
    async def delete(self, cargo_id: int) -> bool:
        """
        Delete a position entity from the database by its ID.

        Args:
            cargo_id: The ID of the position to delete

        Returns:
            True if the position was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, cargo_id: int) -> Cargo:
        """
        Retrieve a position entity from the database by its ID.

        Args:
            cargo_id: The ID of the position to retrieve

        Returns:
            The found position entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of position entities from the database.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing positions and pagination information
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
        Retrieve a paginated list of position entities based on search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with positions matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a position entity exists in the database based on specific criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching position exists, False otherwise
        """
        pass
