from abc import ABC, abstractmethod
from src.app.dto.request import EmployeeRequestDto
from src.app.dto.response import EmployeeResponseDTO, EmployeePage
from src.app.schema import MessageResponse


class IEmployeeService(ABC):
    """
    Interface for employee service operations.
    Defines the contract for employee-related business logic.
    """

    @abstractmethod
    async def add_employee(
        self, employee_request: EmployeeRequestDto
    ) -> EmployeeResponseDTO:
        """
        Add a new employee.

        Args:
            employee_request: The data transfer object containing employee details.

        Returns:
            The created employee as an EmployeeResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_employees(self) -> list[EmployeeResponseDTO]:
        """
        Retrieve all employees.

        Returns:
            A list of EmployeeResponseDTO objects representing all employees.
        """
        pass

    @abstractmethod
    async def update_employee(
        self, employee_id: int, employee_request: EmployeeRequestDto
    ) -> EmployeeResponseDTO:
        """
        Update an existing employee.

        Args:
            employee_id: The ID of the employee to update.
            employee_request: The data transfer object containing updated employee details.

        Returns:
            The updated employee as an EmployeeResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_employee(self, employee_id: int) -> MessageResponse:
        """
        Delete an employee by their ID.

        Args:
            employee_id: The ID of the employee to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_employee_by_id(self, employee_id: int) -> EmployeeResponseDTO:
        """
        Retrieve an employee by their ID.

        Args:
            employee_id: The ID of the employee to retrieve.

        Returns:
            The employee as an EmployeeResponseDTO.
        """
        pass

    @abstractmethod
    async def get_employees_paginated(self, page: int, size: int) -> EmployeePage:
        """
        Retrieve a paginated list of employees.

        Args:
            page: The page number to retrieve.
            size: The number of employees per page.

        Returns:
            An EmployeePage object containing the paginated employees.
        """
        pass

    @abstractmethod
    async def find(
        self, page: int, size: int, search_dict: dict[str, str]
    ) -> EmployeePage:
        """
        Find employees based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of employees per page.
            search_dict: Dictionary of field-value pairs to search for.

        Returns:
            An EmployeePage object containing the employees that match the search criteria.
        """
        pass
