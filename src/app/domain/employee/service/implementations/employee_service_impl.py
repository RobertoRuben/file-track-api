import io
import pandas as pd
from datetime import datetime
from src.app.core.schema import MessageResponse
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.core.helpers import datetime_helper
from src.app.core.exception.decorator import service_handle_exceptions
from src.app.domain.employee.repository.interface import (
    IEmployeeRepository,
    IPositionRepository,
)
from src.app.domain.department.repository.interface import IDepartmentRepository
from src.app.domain.employee.service.interface import IEmployeeService
from src.app.domain.employee.model import Employee
from src.app.domain.employee.dto.request import EmployeeRequestDTO
from src.app.domain.employee.dto.response import EmployeeResponseDTO, EmployeePage


class EmployeeServiceImpl(IEmployeeService):
    """
    Implementation of the Employee Service interface.
    Handles business logic for employee operations.
    """

    def __init__(
        self,
        employee_repository: IEmployeeRepository,
        position_repository: IPositionRepository,
        department_repository: IDepartmentRepository,
    ):
        """
        Initializes the Employee Service with required repositories.

        :param employee_repository: Repository for employee data access
        :param position_repository: Repository for position data access
        :param department_repository: Repository for department data access
        """
        self.employee_repository = employee_repository
        self.position_repository = position_repository
        self.department_repository = department_repository

    @service_handle_exceptions
    async def add_employee(
        self, employee_request: EmployeeRequestDTO
    ) -> EmployeeResponseDTO:
        """
        Adds a new employee to the system.

        :param employee_request: DTO containing the employee details
        :return: DTO with the created employee data
        :raises ConflictException: If an employee with the same DNI already exists
        :raises NotFoundException: If the position or department does not exist
        """
        existing_employee = await self.employee_repository.exists_by(
            dni=employee_request.dni
        )
        if existing_employee:
            raise ConflictException(
                message="Employee already exists",
                details=f"Employee with DNI '{employee_request.dni}' already exists.",
            )

        existing_position = await self.position_repository.exists_by(
            id=employee_request.position_id
        )
        if not existing_position:
            raise NotFoundException(
                message="Position not found",
                details=f"Position with ID {employee_request.position_id} not found.",
            )

        existing_department = await self.department_repository.exists_by(
            id=employee_request.department_id
        )
        if not existing_department:
            raise NotFoundException(
                message="Department not found",
                details=f"Department with ID {employee_request.department_id} not found.",
            )

        new_employee = Employee(
            dni=employee_request.dni,
            names=employee_request.names,
            paternal_surname=employee_request.paternal_surname,
            maternal_surname=employee_request.maternal_surname,
            gender=employee_request.gender.value,
            position_id=employee_request.position_id,
            department_id=employee_request.department_id,
        )

        created_employee = await self.employee_repository.save(new_employee)

        return EmployeeResponseDTO(
            id=created_employee.id,
            dni=created_employee.dni,
            names=created_employee.names,
            paternal_surname=created_employee.paternal_surname,
            maternal_surname=created_employee.maternal_surname,
            gender=created_employee.gender,
            department_id=created_employee.department_id,
            position_id=created_employee.position_id,
            created_at=created_employee.created_at,
            updated_at=created_employee.updated_at,
        )

    @service_handle_exceptions
    async def get_all_employees(self) -> list[EmployeeResponseDTO]:
        """
        Retrieves all employees from the database.

        :return: List of DTOs containing all employees
        """
        employees = await self.employee_repository.get_all()
        return [
            EmployeeResponseDTO(
                id=employee.id,
                dni=employee.dni,
                names=employee.names,
                paternal_surname=employee.paternal_surname,
                maternal_surname=employee.maternal_surname,
                gender=employee.gender,
                department_id=employee.department_id,
                position_id=employee.position_id,
                created_at=employee.created_at,
                updated_at=employee.updated_at,
            )
            for employee in employees
        ]

    @service_handle_exceptions
    async def update_employee(
        self, employee_id: int, employee_request: EmployeeRequestDTO
    ) -> EmployeeResponseDTO:
        """
        Updates an existing employee.

        :param employee_id: ID of the employee to update
        :param employee_request: DTO containing the updated employee details
        :return: DTO with the updated employee data
        :raises NotFoundException: If the employee with the given ID doesn't exist
        :raises ConflictException: If another employee with the same DNI already exists
        :raises NotFoundException: If the position or department does not exist
        """
        exists_employee_id = await self.employee_repository.exists_by(id=employee_id)
        if not exists_employee_id:
            raise NotFoundException(
                message="Employee not found",
                details=f"Employee with ID {employee_id} not found.",
            )

        employee = await self.employee_repository.get_by_id(employee_id)

        if employee.dni != employee_request.dni:
            existing_employee = await self.employee_repository.exists_by(
                dni=employee_request.dni
            )
            if existing_employee:
                raise ConflictException(
                    message="Employee DNI already exists",
                    details=f"Employee with DNI '{employee_request.dni}' already exists.",
                )

        existing_position = await self.position_repository.exists_by(
            id=employee_request.position_id
        )
        if not existing_position:
            raise NotFoundException(
                message="Position not found",
                details=f"Position with ID {employee_request.position_id} not found.",
            )

        existing_department = await self.department_repository.exists_by(
            id=employee_request.department_id
        )
        if not existing_department:
            raise NotFoundException(
                message="Department not found",
                details=f"Department with ID {employee_request.department_id} not found.",
            )

        employee.dni = employee_request.dni
        employee.names = employee_request.names
        employee.paternal_surname = employee_request.paternal_surname
        employee.maternal_surname = employee_request.maternal_surname
        employee.gender = employee_request.gender.value
        employee.position_id = employee_request.position_id
        employee.department_id = employee_request.department_id
        employee.updated_at = datetime.now()

        updated_employee = await self.employee_repository.save(employee)

        return EmployeeResponseDTO(
            id=updated_employee.id,
            dni=updated_employee.dni,
            names=updated_employee.names,
            paternal_surname=updated_employee.paternal_surname,
            maternal_surname=updated_employee.maternal_surname,
            gender=updated_employee.gender,
            department_id=updated_employee.department_id,
            position_id=updated_employee.position_id,
            created_at=updated_employee.created_at,
            updated_at=updated_employee.updated_at,
        )

    @service_handle_exceptions
    async def delete_employee(self, employee_id: int) -> MessageResponse:
        """
        Deletes an employee by their ID.

        :param employee_id: ID of the employee to delete
        :return: Message response indicating success or failure
        :raises NotFoundException: If the employee with the given ID doesn't exist
        """
        existing_employee_id = await self.employee_repository.exists_by(id=employee_id)
        if not existing_employee_id:
            raise NotFoundException(
                message="Employee not found",
                details=f"Employee with ID {employee_id} not found.",
            )

        response = await self.employee_repository.delete(employee_id)

        if response is True:
            return MessageResponse(
                message="Employee deleted successfully.",
                success=True,
                details=f"Employee with ID {employee_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete employee.",
                success=False,
                details=f"Employee with ID {employee_id} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
    async def get_employee_by_id(self, employee_id: int) -> EmployeeResponseDTO:
        """
        Retrieves an employee by their ID.

        :param employee_id: ID of the employee to retrieve
        :return: DTO with the employee data
        :raises NotFoundException: If the employee with the given ID doesn't exist
        """
        existing_employee_id = await self.employee_repository.exists_by(id=employee_id)
        if not existing_employee_id:
            raise NotFoundException(
                message="Employee not found",
                details=f"Employee with ID {employee_id} not found.",
            )

        employee = await self.employee_repository.get_by_id(employee_id)

        return EmployeeResponseDTO(
            id=employee.id,
            dni=employee.dni,
            names=employee.names,
            paternal_surname=employee.paternal_surname,
            maternal_surname=employee.maternal_surname,
            gender=employee.gender,
            department_id=employee.department_id,
            position_id=employee.position_id,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
        )

    @service_handle_exceptions
    async def get_employees_paginated(self, page: int, size: int) -> EmployeePage:
        """
        Retrieves a paginated list of employees.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :return: Paginated employees with metadata
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

        page_result = await self.employee_repository.get_pageable(page, size)
        employee_response = [
            EmployeeResponseDTO(**employee_dict) for employee_dict in page_result.data
        ]
        return EmployeePage(
            data=employee_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> EmployeePage:
        """
        Searches for employees matching the given search criteria.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :param search_term: Term to search for in employee fields
        :return: Paginated employees matching the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no employees match the search criteria
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

        search_dict = {
            "names": search_term,
            "paternal_surname": search_term,
            "maternal_surname": search_term,
            "dni": search_term if search_term and search_term.isdigit() else None,
        }

        page_result = await self.employee_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                message="No employees found",
                details=f"No employees found matching the search term '{search_term}'.",
            )

        employee_response = [
            EmployeeResponseDTO(**employee_dict) for employee_dict in page_result.data
        ]

        return EmployeePage(
            data=employee_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
    async def delete_employees_by_ids(self, employee_ids: list[int]) -> MessageResponse:
        """
        Delete multiple employees by their IDs.

        :param employee_ids: List of employee IDs to delete
        :return: Message with the result of the deletion operation
        :raises BadRequestException: If no IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided IDs do not correspond to existing employees
        """
        if len(employee_ids) == 0:
            raise BadRequestException(
                message="No employee IDs provided",
                details="Please provide a list of employee IDs to delete.",
            )

        invalid_ids = [id for id in employee_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid employee IDs",
                details=f"Employee IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        employees = await self.employee_repository.find_by_ids(employee_ids)

        found_ids = {
            emp["id"] if isinstance(emp, dict) else emp.id for emp in employees
        }
        missing_ids = [id for id in employee_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Employees not found",
                details=f"Employees with IDs {missing_ids} not found. Cannot proceed with deletion.",
            )

        resp = await self.employee_repository.delete_by_ids(employee_ids)

        if resp is True:
            return MessageResponse(
                message="Employees deleted successfully.",
                success=True,
                details=f"Employees with IDs {employee_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete employees.",
                success=False,
                details=f"Employees with IDs {employee_ids} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
    async def export_employees_to_excel(self, employee_ids: list[int]) -> bytes:
        """
        Export employees to Excel format by their IDs.

        :param employee_ids: List of employee IDs to export
        :return: Excel file as bytes
        :raises BadRequestException: If no IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided IDs do not correspond to existing employees
        """

        if len(employee_ids) == 0:
            raise BadRequestException(
                message="No employee IDs provided",
                details="Please provide a list of employee IDs to export.",
            )

        invalid_ids = [id for id in employee_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid employee IDs",
                details=f"Employee IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        employees = await self.employee_repository.find_by_ids(employee_ids)

        found_ids = {
            emp["id"] if isinstance(emp, dict) else emp.id for emp in employees
        }
        missing_ids = [id for id in employee_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Employees not found",
                details=f"Employees with IDs {missing_ids} not found. Cannot proceed with export.",
            )

        employees_data = [
            {
                "ID": employee["id"],
                "DNI": employee["dni"],
                "Names": employee["names"],
                "Paternal Surname": employee["paternal_surname"],
                "Maternal Surname": employee["maternal_surname"],
                "Gender": employee["gender"],
                "Position": employee["position_name"],
                "Department": employee["department_name"],
                "Created At": datetime_helper.to_lima_timezone(employee["created_at"]),
                "Updated At": datetime_helper.to_lima_timezone(employee["updated_at"]),
            }
            for employee in employees
        ]

        df = pd.DataFrame(employees_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Employees", index=False)

            worksheet = writer.sheets["Employees"]
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)

        output.seek(0)
        return output.getvalue()
