from abc import ABC, abstractmethod
from src.app.dto.request import DepartmentRequestDTO
from src.app.dto.response import DepartmentResponseDTO, DepartmentPage
from src.app.schema import MessageResponse


class IDepartmentService(ABC):
    """
    Interface for department service operations.
    Defines the contract for department-related business logic.
    """

    @abstractmethod
    async def add_department(
        self, department_request: DepartmentRequestDTO
    ) -> DepartmentResponseDTO:
        """
        Add a new department.

        :param department_request: The data transfer object containing department details
        :return: The created department as a DepartmentResponseDTO
        :raises ConflictException: If a department with the same name already exists
        """
        pass

    @abstractmethod
    async def get_all_departments(self) -> list[DepartmentResponseDTO]:
        """
        Retrieve all departments.

        :return: A list of DepartmentResponseDTO objects representing all departments
        """
        pass

    @abstractmethod
    async def update_department(
        self, department_id: int, department_request: DepartmentRequestDTO
    ) -> DepartmentResponseDTO:
        """
        Update an existing department.

        :param department_id: The ID of the department to update
        :param department_request: The data transfer object containing updated department details
        :return: The updated department as a DepartmentResponseDTO
        :raises NotFoundException: If the department with the given ID does not exist
        :raises ConflictException: If another department with the same name already exists
        """
        pass

    @abstractmethod
    async def delete_department(self, department_id: int) -> MessageResponse:
        """
        Delete a department by its ID.

        :param department_id: The ID of the department to delete
        :return: A MessageResponse indicating the result of the deletion
        :raises NotFoundException: If the department with the given ID does not exist
        """
        pass

    @abstractmethod
    async def get_department_by_id(self, department_id: int) -> DepartmentResponseDTO:
        """
        Retrieve a department by its ID.

        :param department_id: The ID of the department to retrieve
        :return: The department as a DepartmentResponseDTO
        :raises NotFoundException: If the department with the given ID does not exist
        """
        pass

    @abstractmethod
    async def get_departments_paginated(self, page: int, size: int) -> DepartmentPage:
        """
        Retrieve a paginated list of departments.

        :param page: The page number to retrieve
        :param size: The number of departments per page
        :return: A DepartmentPage object containing the paginated departments
        :raises BadRequestException: If page or size parameters are invalid
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> DepartmentPage:
        """
        Find departments based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of departments per page
        :param search_term: The term to search for in department names
        :return: A DepartmentPage object containing the departments that match the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no departments match the search criteria
        """
        pass

    @abstractmethod
    async def delete_departments_by_ids(
        self, department_ids: list[int]
    ) -> MessageResponse:
        """
        Delete multiple departments by their IDs.

        :param department_ids: List of department IDs to delete
        :return: Message with the result of the deletion operation
        """
        pass

    @abstractmethod
    async def export_departments_to_excel(self, department_ids: list[int]) -> bytes:
        """
        Export departments to Excel format by their IDs.

        :param department_ids: List of department IDs to export
        :return: Excel file as bytes
        """
        pass
