from abc import ABC, abstractmethod
from src.app.dto.request import SettlementRequestDTO
from src.app.dto.response import SettlementResponseDTO, SettlementPage
from src.app.core.schema import MessageResponse


class ISettlementService(ABC):
    """
    Interface for settlement service operations.
    Defines the contract for business logic related to settlements.

    :ivar None: This is an interface and does not have instance variables
    """

    @abstractmethod
    async def add_settlement(
        self, settlement_request: SettlementRequestDTO
    ) -> SettlementResponseDTO:
        """
        Adds a new settlement.

        :param settlement_request: The DTO containing settlement details
        :return: The created settlement as SettlementResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_settlements(self) -> list[SettlementResponseDTO]:
        """
        Retrieves all settlements.

        :return: A list of SettlementResponseDTO objects representing all settlements
        """
        pass

    @abstractmethod
    async def update_settlement(
        self, settlement_id: int, settlement_request: SettlementRequestDTO
    ) -> SettlementResponseDTO:
        """
        Updates an existing settlement.

        :param settlement_id: The ID of the settlement to update
        :param settlement_request: The DTO containing updated settlement details
        :return: The updated settlement as SettlementResponseDTO
        """
        pass

    @abstractmethod
    async def delete_settlement(self, settlement_id: int) -> MessageResponse:
        """
        Deletes a settlement by its ID.

        :param settlement_id: The ID of the settlement to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_settlement_by_id(self, settlement_id: int) -> SettlementResponseDTO:
        """
        Retrieves a settlement by its ID.

        :param settlement_id: The ID of the settlement to retrieve
        :return: The settlement as SettlementResponseDTO
        """
        pass

    @abstractmethod
    async def get_settlements_paginated(self, page: int, size: int) -> SettlementPage:
        """
        Retrieves a paginated list of settlements.

        :param page: The page number to retrieve
        :param size: The number of settlements per page
        :return: A SettlementPage object containing the paginated settlements
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> SettlementPage:
        """
        Searches for settlements based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of settlements per page
        :param search_term: The term to search for in settlement names
        :return: A SettlementPage object containing settlements that match the search criteria
        """
        pass

    @abstractmethod
    async def delete_settlements_by_ids(
        self, settlement_ids: list[int]
    ) -> MessageResponse:
        """
        Deletes multiple settlements by their IDs.

        :param settlement_ids: A list of IDs of the settlements to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def export_settlements_to_excel(self, settlement_ids: list[int]) -> bytes:
        """
        Exports settlements to an Excel file.

        :param settlement_ids: Optional list of settlement IDs to export. If None, exports all settlements.
        :return: Bytes representing the Excel file containing the settlements
        """
        pass
