from abc import ABC, abstractmethod
from src.app.dto.request import EmployeeRequestDTO
from src.app.dto.response import EmployeeResponseDTO, EmployeePage
from src.app.schema import MessageResponse


class IEmployeeService(ABC):
    """
    Interface for employee service operations.
    Defines the contract for employee-related business logic.
    """

    @abstractmethod
    async def add_employee(
        self, employee_request: EmployeeRequestDTO
    ) -> EmployeeResponseDTO:
        """
        Add a new employee.

        :param employee_request: The data transfer object containing employee details
        :return: The created employee as an EmployeeResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_employees(self) -> list[EmployeeResponseDTO]:
        """
        Retrieve all employees.

        :return: A list of EmployeeResponseDTO objects representing all employees
        """
        pass

    @abstractmethod
    async def update_employee(
        self, employee_id: int, employee_request: EmployeeRequestDTO
    ) -> EmployeeResponseDTO:
        """
        Update an existing employee.

        :param employee_id: The ID of the employee to update
        :param employee_request: The data transfer object containing updated employee details
        :return: The updated employee as an EmployeeResponseDTO
        """
        pass

    @abstractmethod
    async def delete_employee(self, employee_id: int) -> MessageResponse:
        """
        Delete an employee by their ID.

        :param employee_id: The ID of the employee to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_employee_by_id(self, employee_id: int) -> EmployeeResponseDTO:
        """
        Retrieve an employee by their ID.

        :param employee_id: The ID of the employee to retrieve
        :return: The employee as an EmployeeResponseDTO
        """
        pass

    @abstractmethod
    async def get_employees_paginated(self, page: int, size: int) -> EmployeePage:
        """
        Retrieve a paginated list of employees.

        :param page: The page number to retrieve
        :param size: The number of employees per page
        :return: An EmployeePage object containing the paginated employees
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> EmployeePage:
        """
        Find employees based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of employees per page
        :param search_term: Dictionary of field-value pairs to search for
        :return: An EmployeePage object containing the employees that match the search criteria
        """
        pass

    @abstractmethod
    async def delete_employees_by_ids(self, employee_ids: list[int]) -> MessageResponse:
        """
        Delete multiple employees by their IDs.

        :param employee_ids: List of employee IDs to delete
        :return: Message with the result of the deletion operation
        """
        pass

    @abstractmethod
    async def export_employees_to_excel(self, employee_ids: list[int]) -> bytes:
        """
        Export employees to Excel format by their IDs.

        :param employee_ids: List of employee IDs to export
        :return: Excel file as bytes
        """
        pass
