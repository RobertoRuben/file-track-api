from abc import ABC, abstractmethod

from src.app.core.schema import Page
from src.app.domain.employee.model import Employee


class IEmployeeRepository(ABC):
    """
    Interface for the Employee repository.

    Defines the contract for operations related to employee data access.
    """

    @abstractmethod
    async def save(self, employee: Employee) -> Employee:
        """
        Saves an employee in the database.

        :param employee: The employee entity to save
        :return: The saved employee with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Employee]:
        """
        Retrieves all employees from the database.

        :return: A list containing all employees
        """
        pass

    @abstractmethod
    async def delete(self, employee_id: int) -> bool:
        """
        Deletes an employee from the database by its ID.

        :param employee_id: The ID of the employee to delete
        :return: True if the employee was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, employee_id: int) -> Employee:
        """
        Retrieves an employee from the database by its ID.

        :param employee_id: The ID of the employee to retrieve
        :return: The found employee entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieves a paginated list of employees from the database.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing employees and pagination information
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

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with employees matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if an employee exists in the database based on specific criteria.

        :param kwargs: Key-value pairs representing search criteria
        :return: True if a matching employee exists, False otherwise
        """
        pass

    @abstractmethod
    async def delete_by_ids(self, employee_ids: list[int]) -> bool:
        """
        Delete multiple employees from the database by their IDs.

        :param employee_ids: List of employee IDs to delete
        :return: True if all employees were successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def find_by_ids(self, employee_ids: list[int]) -> list[dict]:
        """
        Retrieve multiple employees from the database by their IDs.

        :param employee_ids: List of employee IDs to retrieve
        :return: List of employees found with the same fields as returned by get_pageable
        """
        pass
