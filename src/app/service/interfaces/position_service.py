from abc import ABC, abstractmethod
from src.app.dto.request import PositionRequestDTO
from src.app.dto.response import PositionResponseDTO, PositionPage
from src.app.core.schema import MessageResponse


class IPositionService(ABC):
    """
    Interface for position service operations.
    Defines the contract for position-related business logic.
    """

    @abstractmethod
    async def add_position(
        self, position_request: PositionRequestDTO
    ) -> PositionResponseDTO:
        """
        Add a new position.

        :param position_request: The data transfer object containing position details
        :return: The created position as a PositionResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_positions(self) -> list[PositionResponseDTO]:
        """
        Retrieve all positions.

        :return: A list of PositionResponseDTO objects representing all positions
        """
        pass

    @abstractmethod
    async def update_position(
        self, position_id: int, position_request: PositionRequestDTO
    ) -> PositionResponseDTO:
        """
        Update an existing position.

        :param position_id: The ID of the position to update
        :param position_request: The data transfer object containing updated position details
        :return: The updated position as a PositionResponseDTO
        """
        pass

    @abstractmethod
    async def delete_position(self, position_id: int) -> MessageResponse:
        """
        Delete a position by its ID.

        :param position_id: The ID of the position to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_position_by_id(self, position_id: int) -> PositionResponseDTO:
        """
        Retrieve a position by its ID.

        :param position_id: The ID of the position to retrieve
        :return: The position as a PositionResponseDTO
        """
        pass

    @abstractmethod
    async def get_positions_paginated(self, page: int, size: int) -> PositionPage:
        """
        Retrieve a paginated list of positions.

        :param page: The page number to retrieve
        :param size: The number of positions per page
        :return: A PositionPage object containing the paginated positions
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> PositionPage:
        """
        Find positions based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of positions per page
        :param search_term: The term to search for in position names
        :return: A PositionPage object containing the positions that match the search criteria
        """
        pass

    @abstractmethod
    async def delete_positions_by_ids(self, position_ids: list[int]) -> MessageResponse:
        """
        Delete multiple positions by their IDs.

        :param position_ids: List of position IDs to delete
        :return: Message with the result of the deletion operation
        """
        pass

    @abstractmethod
    async def export_positions_to_excel(self, position_ids: list[int]) -> bytes:
        """
        Export positions to Excel format by their IDs.

        :param position_ids: List of position IDs to export
        :return: Excel file as bytes
        """
        pass
