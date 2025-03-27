from abc import ABC, abstractmethod
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDto, HamletPage
from src.app.schema import MessageResponse


class IHamletService(ABC):
    """
    Interface for hamlet service operations.
    Defines the contract for business logic related to hamlets.
    """

    @abstractmethod
    async def add_hamlet(self, hamlet_request: HamletRequestDTO) -> HamletResponseDto:
        """
        Adds a new hamlet.

        Args:
            hamlet_request: The DTO containing hamlet details.

        Returns:
            The created hamlet as HamletResponseDto.
        """
        pass

    @abstractmethod
    async def get_all_hamlets(self) -> list[HamletResponseDto]:
        """
        Retrieves all hamlets.

        Returns:
            A list of HamletResponseDto objects representing all hamlets.
        """
        pass

    @abstractmethod
    async def update_hamlet(
        self, hamlet_id: int, hamlet_request: HamletRequestDTO
    ) -> HamletResponseDto:
        """
        Updates an existing hamlet.

        Args:
            hamlet_id: The ID of the hamlet to update.
            hamlet_request: The DTO containing updated hamlet details.

        Returns:
            The updated hamlet as HamletResponseDto.
        """
        pass

    @abstractmethod
    async def delete_hamlet(self, hamlet_id: int) -> MessageResponse:
        """
        Deletes a hamlet by its ID.

        Args:
            hamlet_id: The ID of the hamlet to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_hamlet_by_id(self, hamlet_id: int) -> HamletResponseDto:
        """
        Retrieves a hamlet by its ID.

        Args:
            hamlet_id: The ID of the hamlet to retrieve.

        Returns:
            The hamlet as HamletResponseDto.
        """
        pass

    @abstractmethod
    async def get_hamlets_paginated(self, page: int, size: int) -> HamletPage:
        """
        Retrieves a paginated list of hamlets.

        Args:
            page: The page number to retrieve.
            size: The number of hamlets per page.

        Returns:
            A HamletPage object containing the paginated hamlets.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> HamletPage:
        """
        Searches for hamlets based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of hamlets per page.
            search_term: The term to search for in hamlet names.

        Returns:
            A HamletPage object containing hamlets that match the search criteria.
        """
        pass
