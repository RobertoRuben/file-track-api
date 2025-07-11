from abc import ABC, abstractmethod
from src.app.core.security.auth.model import CurrentUser
from src.app.core.schema import MessageResponse
from src.app.domain.department.dto.request import DepartmentConnectionRequestDTO
from src.app.domain.department.dto.response import (
    DepartmentConnectionResponseDTO,
    DepartmentConnectionPage,
)


class IDepartmentConnectionService(ABC):
    """
    Interface for department connection service operations.
    Defines the contract for department connection-related business logic.
    """

    @abstractmethod
    async def add_department_connection(
        self, department_connection_request: DepartmentConnectionRequestDTO
    ) -> DepartmentConnectionResponseDTO:
        """
        Add a new department connection.

        :param department_connection_request: The data transfer object containing department connection details
        :return: The created department connection as a DepartmentConnectionResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_department_connections(
        self,
    ) -> list[DepartmentConnectionResponseDTO]:
        """
        Retrieve all department connections.

        :return: A list of DepartmentConnectionResponseDTO objects representing all department connections
        """
        pass

    @abstractmethod
    async def update_department_connection(
        self,
        department_connection_id: int,
        department_connection_request: DepartmentConnectionRequestDTO,
    ) -> DepartmentConnectionResponseDTO:
        """
        Update an existing department connection.

        :param department_connection_id: The ID of the department connection to update
        :param department_connection_request: The data transfer object containing updated department connection details
        :return: The updated department connection as a DepartmentConnectionResponseDTO
        """
        pass

    @abstractmethod
    async def delete_department_connection(
        self, department_connection_id: int
    ) -> MessageResponse:
        """
        Delete a department connection by its ID.

        :param department_connection_id: The ID of the department connection to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_department_connection_by_id(
        self, department_connection_id: int
    ) -> DepartmentConnectionResponseDTO:
        """
        Retrieve a department connection by its ID.

        :param department_connection_id: The ID of the department connection to retrieve
        :return: The department connection as a DepartmentConnectionResponseDTO
        """
        pass

    @abstractmethod
    async def get_paginated_department_connections(
        self, page: int, size: int
    ) -> DepartmentConnectionPage:
        """
        Retrieve a paginated list of department connections.

        :param page: The page number to retrieve
        :param size: The number of department connections per page
        :return: A DepartmentConnectionPage object containing the paginated department connections
        """
        pass

    @abstractmethod
    async def find(
        self, page: int, size: int, search_term: str
    ) -> DepartmentConnectionPage:
        """
        Find department connections based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of department connections per page
        :param search_term: The term to search for in department connection details
        :return: A DepartmentConnectionPage object containing the department connections that match the search criteria
        """
        pass

    @abstractmethod
    async def get_connections_by_source_department_id(
        self, source_department_id: int
    ) -> list[DepartmentConnectionResponseDTO]:
        """
        Retrieve department connections by source department ID.

        :param source_department_id: The ID of the source department to filter connections
        :return: A list of DepartmentConnectionResponseDTO objects representing connections with the specified source department ID
        """
        pass

    @abstractmethod
    async def get_department_connections_by_current_user_department(
        self, current_user: CurrentUser
    ) -> list[DepartmentConnectionResponseDTO]:
        """
        Retrieve department connections by the current user's department.

        :param current_user: The current user object containing department information
        :return: A list of DepartmentConnectionResponseDTO objects representing connections for the current user's department
        """
        pass
