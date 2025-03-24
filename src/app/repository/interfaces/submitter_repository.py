from abc import ABC, abstractmethod
from src.app.model.entity import Remitente
from src.app.schema import Page


class ISubmitterRepository(ABC):
    """
    Interface for the Remitente (Sender) repository.
    """

    @abstractmethod
    async def save(self, remitente: Remitente) -> Remitente:
        """
        Save a sender.

        Args:
            remitente: The sender to save

        Returns:
            The saved sender with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Remitente]:
        """
        Get all senders.

        Returns:
            A list containing all senders
        """
        pass

    @abstractmethod
    async def delete(self, remitente_id: int) -> bool:
        """
        Delete a sender by its ID.

        Args:
            remitente_id: The ID of the sender to delete

        Returns:
            True if the sender was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, remitente_id: int) -> Remitente:
        """
        Get a sender by its ID.

        Args:
            remitente_id: The ID of the sender to retrieve

        Returns:
            The found sender
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Get a paginated list of senders.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing senders and pagination information
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
        Find senders by search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with senders matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a sender exists based on the given criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching sender exists, False otherwise
        """
        pass
