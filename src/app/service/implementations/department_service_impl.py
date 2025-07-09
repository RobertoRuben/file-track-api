import pandas as pd
import io
from datetime import datetime
from src.app.model.entity import Department
from src.app.service.helpers import datetime_helper
from src.app.dto.request import DepartmentRequestDTO
from src.app.dto.response import DepartmentPage, DepartmentResponseDTO
from src.app.core.schema import MessageResponse
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.core.exception import handle_exceptions
from src.app.repository.interfaces import IDepartmentRepository
from src.app.service.interfaces import IDepartmentService


class DepartmentServiceImpl(IDepartmentService):
    """
    Implementation of the department service interface.
    Handles business logic for department operations.

    :ivar department_repository: Repository for department data operations
    """

    def __init__(self, department_repository: IDepartmentRepository):
        """
        Initialize the department service with a repository.

        :param department_repository: Repository for department data operations
        """
        self.department_repository = department_repository

    @handle_exceptions
    async def add_department(
        self, department_request: DepartmentRequestDTO
    ) -> DepartmentResponseDTO:
        """
        Add a new department.

        :param department_request: The data transfer object containing department details
        :return: The created department as a DepartmentResponseDTO
        :raises ConflictException: If a department with the same name already exists
        """
        existing_department = await self.department_repository.exists_by(
            name=department_request.name
        )
        if existing_department:
            raise ConflictException(
                message="Department already exists",
                details=f"Department with name '{department_request.name}' already exists.",
            )

        new_department = Department(
            name=department_request.name,
        )

        created_department = await self.department_repository.save(new_department)

        return DepartmentResponseDTO(
            id=created_department.id,
            name=created_department.name,
            created_at=created_department.created_at,
            updated_at=created_department.updated_at,
        )

    @handle_exceptions
    async def get_all_departments(self) -> list[DepartmentResponseDTO]:
        """
        Retrieve all departments.

        :return: A list of DepartmentResponseDTO objects representing all departments
        """
        departments = await self.department_repository.get_all()
        return [
            DepartmentResponseDTO(
                id=department.id,
                name=department.name,
                created_at=department.created_at,
                updated_at=department.updated_at,
            )
            for department in departments
        ]

    @handle_exceptions
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
        exists_department_id = await self.department_repository.exists_by(
            id=department_id
        )
        if not exists_department_id:
            raise NotFoundException(
                message="Department not found",
                details=f"Department with ID {department_id} not found.",
            )

        department = await self.department_repository.get_by_id(department_id)

        if department.name != department_request.name:
            existing_department = await self.department_repository.exists_by(
                name=department_request.name
            )
            if existing_department:
                raise ConflictException(
                    message="Department name already exists",
                    details=f"Department with name '{department_request.name}' already exists.",
                )

        department.name = department_request.name
        department.updated_at = datetime.now()

        updated_department = await self.department_repository.save(department)

        return DepartmentResponseDTO(
            id=updated_department.id,
            name=updated_department.name,
            created_at=updated_department.created_at,
            updated_at=updated_department.updated_at,
        )

    @handle_exceptions
    async def delete_department(self, department_id: int) -> MessageResponse:
        """
        Delete a department by its ID.

        :param department_id: The ID of the department to delete
        :return: A MessageResponse indicating the result of the deletion
        :raises NotFoundException: If the department with the given ID does not exist
        """
        existing_department_id = await self.department_repository.exists_by(
            id=department_id
        )
        if not existing_department_id:
            raise NotFoundException(
                message="Department not found",
                details=f"Department with ID {department_id} not found.",
            )

        response = await self.department_repository.delete(department_id)
        if response is True:
            return MessageResponse(
                message="Department deleted successfully.",
                success=True,
                details=f"Department with ID {department_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete department.",
                success=False,
                details=f"Department with ID {department_id} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def get_department_by_id(self, department_id: int) -> DepartmentResponseDTO:
        """
        Retrieve a department by its ID.

        :param department_id: The ID of the department to retrieve
        :return: The department as a DepartmentResponseDTO
        :raises NotFoundException: If the department with the given ID does not exist
        """
        existing_department_id = await self.department_repository.exists_by(
            id=department_id
        )
        if not existing_department_id:
            raise NotFoundException(
                message="Department not found",
                details=f"Department with ID {department_id} not found.",
            )

        department = await self.department_repository.get_by_id(department_id)
        return DepartmentResponseDTO(
            id=department.id,
            name=department.name,
            created_at=department.created_at,
            updated_at=department.updated_at,
        )

    @handle_exceptions
    async def get_departments_paginated(self, page: int, size: int) -> DepartmentPage:
        """
        Retrieve a paginated list of departments.

        :param page: The page number to retrieve
        :param size: The number of departments per page
        :return: A DepartmentPage object containing the paginated departments
        :raises BadRequestException: If page or size parameters are invalid
        """
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid page size",
                details="Page size must be greater than 0.",
            )

        page_result = await self.department_repository.get_pageable(page, size)

        department_response = [
            DepartmentResponseDTO(
                id=department.id,
                name=department.name,
                created_at=department.created_at,
                updated_at=department.updated_at,
            )
            for department in page_result.data
        ]

        return DepartmentPage(
            data=department_response,
            meta=page_result.meta,
        )

    @handle_exceptions
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
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid page size",
                details="Page size must be greater than 0.",
            )

        search_dict = {"name": search_term}

        page_result = await self.department_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                message="No departments found",
                details=f"No departments found matching the search term '{search_term}'.",
            )

        department_response = [
            DepartmentResponseDTO(
                id=department.id,
                name=department.name,
                created_at=department.created_at,
                updated_at=department.updated_at,
            )
            for department in page_result.data
        ]

        return DepartmentPage(
            data=department_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def delete_departments_by_ids(
        self, department_ids: list[int]
    ) -> MessageResponse:
        """
        Delete multiple departments by their IDs.

        :param department_ids: List of department IDs to delete
        :return: Message with the result of the deletion operation
        :raises BadRequestException: If no IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided IDs do not correspond to existing departments
        """

        if len(department_ids) == 0:
            raise BadRequestException(
                message="No department IDs provided",
                details="Please provide a list of department IDs to delete.",
            )

        invalid_ids = [id for id in department_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid department IDs",
                details=f"Department IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        departments = await self.department_repository.find_by_ids(department_ids)

        found_ids = {
            dep["id"] if isinstance(dep, dict) else dep.id for dep in departments
        }
        missing_ids = [id for id in department_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Departments not found",
                details=f"Departments with IDs {missing_ids} not found. Cannot proceed with deletion.",
            )

        resp = await self.department_repository.delete_by_ids(department_ids)

        if resp is True:
            return MessageResponse(
                message="Departments deleted successfully.",
                success=True,
                details=f"Departments with IDs {department_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete departments.",
                success=False,
                details=f"Departments with IDs {department_ids} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def export_departments_to_excel(self, department_ids: list[int]) -> bytes:
        """
        Export departments to Excel format by their IDs.

        :param department_ids: List of department IDs to export
        :return: Excel file as bytes
        :raises BadRequestException: If no IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided IDs do not correspond to existing departments
        """
        if len(department_ids) == 0:
            raise BadRequestException(
                message="No department IDs provided",
                details="Please provide a list of department IDs to export.",
            )

        invalid_ids = [id for id in department_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid department IDs",
                details=f"Department IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        departments = await self.department_repository.find_by_ids(department_ids)

        found_ids = {
            dep["id"] if isinstance(dep, dict) else dep.id for dep in departments
        }
        missing_ids = [id for id in department_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Departments not found",
                details=f"Departments with IDs {missing_ids} not found. Cannot proceed with export.",
            )

        departments_data = [
            {
                "ID": department.id,
                "Nombre": department.name,
                "Fecha de Creación": datetime_helper.to_lima_timezone(
                    department.created_at
                ),
                "Fecha de Actualización": datetime_helper.to_lima_timezone(
                    department.updated_at
                ),
            }
            for department in departments
        ]

        df = pd.DataFrame(departments_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Departments", index=False)

            worksheet = writer.sheets["Departments"]
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)

        output.seek(0)
        return output.getvalue()
