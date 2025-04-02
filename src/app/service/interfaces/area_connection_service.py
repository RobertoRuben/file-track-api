from abc import ABC, abstractmethod
from src.app.dto.request import AreaConnectionRequestDto
from src.app.dto.response import AreaConnectionResponseDTO, AreaConnectionPage
from src.app.schema import MessageResponse


class IAreaConnectionService(ABC):
    """
    Interface for department connection service operations.
    Defines the contract for department connection-related business logic.
    """

    @abstractmethod
    async def add_area_connection(
        self, area_connection_request: AreaConnectionRequestDto
    ) -> AreaConnectionResponseDTO:
        """
        Add a new department connection.

        Args:
            area_connection_request: The data transfer object containing department connection details.

        Returns:
            The created department connection as an AreaConnectionResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_area_connections(self) -> list[AreaConnectionResponseDTO]:
        """
        Retrieve all department connections.

        Returns:
            A list of AreaConnectionResponseDTO objects representing all department connections.
        """
        pass

    @abstractmethod
    async def update_area_connection(
        self,
        area_connection_id: int,
        area_connection_request: AreaConnectionRequestDto,
    ) -> AreaConnectionResponseDTO:
        """
        Update an existing department connection.

        Args:
            area_connection_id: The ID of the department connection to update.
            area_connection_request: The data transfer object containing updated department connection details.

        Returns:
            The updated department connection as an AreaConnectionResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_area_connection(self, area_connection_id: int) -> MessageResponse:
        """
        Delete a department connection by its ID.

        Args:
            area_connection_id: The ID of the department connection to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_area_connection_by_id(
        self, area_connection_id: int
    ) -> AreaConnectionResponseDTO:
        """
        Retrieve a department connection by its ID.

        Args:
            area_connection_id: The ID of the department connection to retrieve.

        Returns:
            The department connection as an AreaConnectionResponseDTO.
        """
        pass

    @abstractmethod
    async def get_paginated_area_connections(
        self, page: int, size: int
    ) -> AreaConnectionPage:
        """
        Retrieve a paginated list of department connections.

        Args:
            page: The page number to retrieve.
            size: The number of department connections per page.

        Returns:
            An AreaConnectionPage object containing the paginated department connections.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> AreaConnectionPage:
        """
        Find department connections based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of department connections per page.
            search_term: The term to search for in department connection details.

        Returns:
            An AreaConnectionPage object containing the department connections that match the search criteria.
        """
        pass

    @abstractmethod
    async def get_connections_by_area_origen_id(
        self, area_origen_id: int
    ) -> list[AreaConnectionResponseDTO]:
        """
        Retrieve department connections by area origin ID.

        Args:
            area_origen_id: The ID of the area origin to filter department connections.

        Returns:
            A list of AreaConnectionResponseDTO objects representing department connections with the specified area origin ID.
        """
        pass
