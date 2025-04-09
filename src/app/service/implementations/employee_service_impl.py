from datetime import datetime
from src.app.model.entity import Employee
from src.app.dto.request import EmployeeRequestDTO
from src.app.dto.response import EmployeeResponseDTO, EmployeePage
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IEmployeeRepository
from src.app.repository.interfaces import IPositionRepository
from src.app.repository.interfaces import IDepartmentRepository
from src.app.service.interfaces import IEmployeeService


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

    @handle_exceptions
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
                details=f"Employee with DNI {employee_request.dni} already exists",
            )
        existing_position = await self.position_repository.exists_by(
            id=employee_request.position_id
        )
        if not existing_position:
            raise NotFoundException(
                details=f"Position with ID {employee_request.position_id} does not exist",
            )
        existing_department = await self.department_repository.exists_by(
            id=employee_request.department_id
        )
        if not existing_department:
            raise NotFoundException(
                details=f"Department with ID {employee_request.department_id} does not exist",
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

    @handle_exceptions
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

    @handle_exceptions
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
                details=f"Employee with id {employee_id} not found",
            )

        employee = await self.employee_repository.get_by_id(employee_id)

        if employee.dni != employee_request.dni:
            existing_employee = await self.employee_repository.exists_by(
                dni=employee_request.dni
            )
            if existing_employee:
                raise ConflictException(
                    details=f"Employee with DNI {employee_request.dni} already exists",
                )

        existing_position = await self.position_repository.exists_by(
            id=employee_request.position_id
        )
        if not existing_position:
            raise NotFoundException(
                details=f"Position with ID {employee_request.position_id} does not exist",
            )

        existing_department = await self.department_repository.exists_by(
            id=employee_request.department_id
        )
        if not existing_department:
            raise NotFoundException(
                details=f"Department with ID {employee_request.department_id} does not exist",
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

    @handle_exceptions
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
                details=f"Employee with id {employee_id} not found",
            )

        response = await self.employee_repository.delete(employee_id)

        if response is True:
            return MessageResponse(
                message="Employee deleted successfully.",
                success=True,
                details=f"Employee with id {employee_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete employee.",
                success=False,
                details=f"Employee with id {employee_id} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
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
                details=f"Employee with id {employee_id} not found",
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

    @handle_exceptions
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
                details="Page number must be greater than 0",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid size number",
                details="Size number must be greater than 0",
            )

        page_result = await self.employee_repository.get_pageable(page, size)
        employee_response = [
            EmployeeResponseDTO(**employee_dict) for employee_dict in page_result.data
        ]
        return EmployeePage(
            data=employee_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> EmployeePage:
        """
        Searches for employees matching the given search criteria.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :param search_term: Dictionary with field names and search terms
        :return: Paginated employees matching the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no employees match the search criteria
        """
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid size number",
                details="Size number must be greater than 0",
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
                details="No employees found with the provided search criteria",
            )

        employee_response = [
            EmployeeResponseDTO(**employee_dict) for employee_dict in page_result.data
        ]

        return EmployeePage(
            data=employee_response,
            meta=page_result.meta,
        )
