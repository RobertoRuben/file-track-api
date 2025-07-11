from abc import ABC, abstractmethod

from src.app.core.schema import Page
from src.app.domain.department.model import DepartmentConnection


class IDepartmentConnectionRepository(ABC):
    """
    Interface for the Department Connection repository.
    Defines the contract for data access operations related to connections between departments.
    """

    @abstractmethod
    async def save(
        self, department_connection: DepartmentConnection
    ) -> DepartmentConnection:
        """
        Saves a department connection.

        :param department_connection: The department connection to save
        :return: The saved department connection with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[DepartmentConnection]:
        """
        Gets all department connections.

        :return: A list with all department connections
        """
        pass

    @abstractmethod
    async def delete(self, department_connection_id: int) -> bool:
        """
        Deletes a department connection by its ID.

        :param department_connection_id: The ID of the department connection to delete
        :return: True if the connection was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, department_connection_id: int) -> DepartmentConnection:
        """
        Gets a department connection by its ID.

        :param department_connection_id: The ID of the department connection to retrieve
        :return: The found department connection
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Gets a paginated list of department connections.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing department connections and pagination information
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
        Searches for department connections according to search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with department connections that match the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if a department connection exists according to given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching department connection exists, False otherwise
        """
        pass

    @abstractmethod
    async def get_connections_by_source_department_id(
        self, source_department_id: int
    ) -> list[DepartmentConnection]:
        """
        Gets all department connections by source department ID.

        :param source_department_id: The ID of the source department to filter connections
        :return: A list with all department connections that match the source department ID
        """
        pass
