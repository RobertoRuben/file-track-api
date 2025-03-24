from abc import ABC, abstractmethod
from src.app.dto.request import PositionRequestDTO
from src.app.dto.response import PositionResponseDTO, PositionPage
from src.app.schema import MessageResponse


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

        Args:
            position_request: The data transfer object containing position details.

        Returns:
            The created position as a PositionResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_positions(self) -> list[PositionResponseDTO]:
        """
        Retrieve all positions.

        Returns:
            A list of PositionResponseDTO objects representing all positions.
        """
        pass

    @abstractmethod
    async def update_position(
        self, position_id: int, position_request: PositionRequestDTO
    ) -> PositionResponseDTO:
        """
        Update an existing position.

        Args:
            position_id: The ID of the position to update.
            position_request: The data transfer object containing updated position details.

        Returns:
            The updated position as a PositionResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_position(self, position_id: int) -> MessageResponse:
        """
        Delete a position by its ID.

        Args:
            position_id: The ID of the position to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_position_by_id(self, position_id: int) -> PositionResponseDTO:
        """
        Retrieve a position by its ID.

        Args:
            position_id: The ID of the position to retrieve.

        Returns:
            The position as a PositionResponseDTO.
        """
        pass

    @abstractmethod
    async def get_positions_paginated(self, page: int, size: int) -> PositionPage:
        """
        Retrieve a paginated list of positions.

        Args:
            page: The page number to retrieve.
            size: The number of positions per page.

        Returns:
            A PositionPage object containing the paginated positions.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> PositionPage:
        """
        Find positions based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of positions per page.
            search_term: The term to search for in position names.

        Returns:
            A PositionPage object containing the positions that match the search criteria.
        """
        pass
