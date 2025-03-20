from abc import ABC, abstractmethod
from src.app.model.entity import Ambito
from src.app.schema import Page

class IDocumentaryTopicRepository(ABC):
    """
    Interface for the Documentary Topic repository.
    """

    @abstractmethod
    async def save(self, ambito: Ambito) -> Ambito:
        """
        Save a documentary topic.

        Args:
            ambito: The documentary topic to save

        Returns:
            The saved documentary topic with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Ambito]:
        """
        Get all documentary topics.

        Returns:
            A list containing all documentary topics
        """
        pass

    @abstractmethod
    async def delete(self, ambito_id: int) -> bool:
        """
        Delete a documentary topic by its ID.

        Args:
            ambito_id: The ID of the documentary topic to delete

        Returns:
            True if the topic was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, ambito_id: int) -> Ambito:
        """
        Get a documentary topic by its ID.

        Args:
            ambito_id: The ID of the documentary topic to retrieve

        Returns:
            The found documentary topic
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Get a paginated list of documentary topics.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing documentary topics and pagination information
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
        Find documentary topics by search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with documentary topics matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a documentary topic exists based on the given criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching documentary topic exists, False otherwise
        """
        pass