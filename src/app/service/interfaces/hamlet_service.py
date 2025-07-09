from abc import ABC, abstractmethod
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDTO, HamletPage
from src.app.core.schema import MessageResponse


class IHamletService(ABC):
    """
    Interface for hamlet service operations.
    Defines the contract for business logic related to hamlets.
    """

    @abstractmethod
    async def add_hamlet(self, hamlet_request: HamletRequestDTO) -> HamletResponseDTO:
        """
        Adds a new hamlet.

        :param hamlet_request: The DTO containing hamlet details
        :return: The created hamlet as HamletResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_hamlets(self) -> list[HamletResponseDTO]:
        """
        Retrieves all hamlets.

        :return: A list of HamletResponseDTO objects representing all hamlets
        """
        pass

    @abstractmethod
    async def update_hamlet(
        self, hamlet_id: int, hamlet_request: HamletRequestDTO
    ) -> HamletResponseDTO:
        """
        Updates an existing hamlet.

        :param hamlet_id: The ID of the hamlet to update
        :param hamlet_request: The DTO containing updated hamlet details
        :return: The updated hamlet as HamletResponseDTO
        """
        pass

    @abstractmethod
    async def delete_hamlet(self, hamlet_id: int) -> MessageResponse:
        """
        Deletes a hamlet by its ID.

        :param hamlet_id: The ID of the hamlet to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_hamlet_by_id(self, hamlet_id: int) -> HamletResponseDTO:
        """
        Retrieves a hamlet by its ID.

        :param hamlet_id: The ID of the hamlet to retrieve
        :return: The hamlet as HamletResponseDTO
        """
        pass

    @abstractmethod
    async def get_hamlets_paginated(self, page: int, size: int) -> HamletPage:
        """
        Retrieves a paginated list of hamlets.

        :param page: The page number to retrieve
        :param size: The number of hamlets per page
        :return: A HamletPage object containing the paginated hamlets
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> HamletPage:
        """
        Searches for hamlets based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of hamlets per page
        :param search_term: The term to search for in hamlet names
        :return: A HamletPage object containing hamlets that match the search criteria
        """
        pass

    @abstractmethod
    async def delete_hamlets_by_ids(self, hamlet_ids: list[int]) -> MessageResponse:
        """
        Delete multiple hamlets by their IDs.

        :param hamlet_ids: List of hamlet IDs to delete
        :return: Message with the result of the deletion operation
        """
        pass

    @abstractmethod
    async def export_hamlets_to_excel(self, hamlet_ids: list[int]) -> bytes:
        """
        Export hamlets to Excel format by their IDs.

        :param hamlet_ids: List of hamlet IDs to export
        :return: Excel file as bytes
        """
        pass
