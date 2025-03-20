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
    async def add_department(self, department_request: DepartmentRequestDTO) -> DepartmentResponseDTO:
        """
        Add a new department.

        Args:
            department_request: The data transfer object containing department details.

        Returns:
            The created department as a DepartmentResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_departments(self) -> list[DepartmentResponseDTO]:
        """
        Retrieve all departments.

        Returns:
            A list of DepartmentResponseDTO objects representing all departments.
        """
        pass

    @abstractmethod
    async def update_department(self, department_id: int, department_request: DepartmentRequestDTO) -> DepartmentResponseDTO:
        """
        Update an existing department.

        Args:
            department_id: The ID of the department to update.
            department_request: The data transfer object containing updated department details.

        Returns:
            The updated department as a DepartmentResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_department(self, department_id: int) -> MessageResponse:
        """
        Delete a department by its ID.

        Args:
            department_id: The ID of the department to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_department_by_id(self, department_id: int) -> DepartmentResponseDTO:
        """
        Retrieve a department by its ID.

        Args:
            department_id: The ID of the department to retrieve.

        Returns:
            The department as a DepartmentResponseDTO.
        """
        pass

    @abstractmethod
    async def get_departments_paginated(self, page: int, size: int) -> DepartmentPage:
        """
        Retrieve a paginated list of departments.

        Args:
            page: The page number to retrieve.
            size: The number of departments per page.

        Returns:
            A DepartmentPage object containing the paginated departments.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> DepartmentPage:
        """
        Find departments based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of departments per page.
            search_term: The term to search for in department names.

        Returns:
            A DepartmentPage object containing the departments that match the search criteria.
        """
        pass