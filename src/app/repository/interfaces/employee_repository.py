from abc import ABC, abstractmethod
from src.app.model.entity import Trabajador
from src.app.schema import Page


class IEmployeeRepository(ABC):
    """
    Interface for the Employee repository.
    """

    @abstractmethod
    async def save(self, trabajador: Trabajador) -> Trabajador:
        """
        Saves an employee in the database.

        Args:
            trabajador: The employee entity to save

        Returns:
            The saved employee with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Trabajador]:
        """
        Retrieves all employees from the database.

        Returns:
            A list containing all employees
        """
        pass

    @abstractmethod
    async def delete(self, trabajador_id: int) -> bool:
        """
        Deletes an employee from the database by its ID.

        Args:
            trabajador_id: The ID of the employee to delete

        Returns:
            True if the employee was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, trabajador_id: int) -> Trabajador:
        """
        Retrieves an employee from the database by its ID.

        Args:
            trabajador_id: The ID of the employee to retrieve

        Returns:
            The found employee entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieves a paginated list of employees from the database.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing employees and pagination information
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
        Retrieves a paginated list of employees based on search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with employees matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if an employee exists in the database based on specific criteria.

        Args:
            **kwargs: Key-value pairs representing search criteria

        Returns:
            True if a matching employee exists, False otherwise
        """
        pass
