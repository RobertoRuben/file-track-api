from abc import ABC, abstractmethod
from src.app.model.entity import Position
from src.app.schema import Page


class IPositionRepository(ABC):
    """
    Interface for the Position repository.
    """

    @abstractmethod
    async def save(self, position: Position) -> Position:
        """
        Save a position entity to the database.

        :param position: The position entity to save
        :return: The saved position with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Position]:
        """
        Retrieve all position entities from the database.

        :return: A list containing all positions
        """
        pass

    @abstractmethod
    async def delete(self, position_id: int) -> bool:
        """
        Delete a position entity from the database by its ID.

        :param position_id: The ID of the position to delete
        :return: True if the position was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, position_id: int) -> Position:
        """
        Retrieve a position entity from the database by its ID.

        :param position_id: The ID of the position to retrieve
        :return: The found position entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of position entities from the database.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing positions and pagination information
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

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with positions matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a position entity exists in the database based on specific criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching position exists, False otherwise
        """
        pass
