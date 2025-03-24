from abc import ABC, abstractmethod
from src.app.dto.request import SettlementRequestDTO
from src.app.dto.response import SettlementReponseDTO, SettlementPage
from src.app.schema import MessageResponse


class ISettlementService(ABC):
    """
    Interface for settlement service operations.
    Defines the contract for business logic related to settlements.
    """

    @abstractmethod
    async def add_settlement(
        self, settlement_request: SettlementRequestDTO
    ) -> SettlementReponseDTO:
        """
        Adds a new settlement.

        Args:
            settlement_request: The DTO containing settlement details.

        Returns:
            The created settlement as SettlementReponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_settlements(self) -> list[SettlementReponseDTO]:
        """
        Retrieves all settlements.

        Returns:
            A list of SettlementReponseDTO objects representing all settlements.
        """
        pass

    @abstractmethod
    async def update_settlement(
        self, settlement_id: int, settlement_request: SettlementRequestDTO
    ) -> SettlementReponseDTO:
        """
        Updates an existing settlement.

        Args:
            settlement_id: The ID of the settlement to update.
            settlement_request: The DTO containing updated settlement details.

        Returns:
            The updated settlement as SettlementReponseDTO.
        """
        pass

    @abstractmethod
    async def delete_settlement(self, settlement_id: int) -> MessageResponse:
        """
        Deletes a settlement by its ID.

        Args:
            settlement_id: The ID of the settlement to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_settlement_by_id(self, settlement_id: int) -> SettlementReponseDTO:
        """
        Retrieves a settlement by its ID.

        Args:
            settlement_id: The ID of the settlement to retrieve.

        Returns:
            The settlement as SettlementReponseDTO.
        """
        pass

    @abstractmethod
    async def get_settlements_paginated(self, page: int, size: int) -> SettlementPage:
        """
        Retrieves a paginated list of settlements.

        Args:
            page: The page number to retrieve.
            size: The number of settlements per page.

        Returns:
            A SettlementPage object containing the paginated settlements.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> SettlementPage:
        """
        Searches for settlements based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of settlements per page.
            search_term: The term to search for in settlement names.

        Returns:
            A SettlementPage object containing settlements that match the search criteria.
        """
        pass
