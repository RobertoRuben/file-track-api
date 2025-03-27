from datetime import datetime
from src.app.model.entity import Trabajador
from src.app.dto.request import EmployeeRequestDto
from src.app.dto.response import EmployeeResponseDTO, EmployeePage
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IEmployeeRepository
from src.app.repository.interfaces import IPositionRepository
from src.app.repository.interfaces import IAreaRepository
from src.app.service.interfaces import IEmployeeService


class EmployeeServiceImpl(IEmployeeService):
    """
    Implementation of the Employee Service interface.
    Handles business logic for employee operations.
    """

    def __init__(
        self,
        repository: IEmployeeRepository,
        position_repository: IPositionRepository,
        area_repository: IAreaRepository,
    ):
        """
        Initializes the Employee Service with required repositories.

        Args:
            repository: Repository for employee data access
            position_repository: Repository for position data access
            area_repository: Repository for area/department data access
        """
        self.repository = repository
        self.position_repository = position_repository
        self.area_repository = area_repository

    @handle_exceptions
    async def add_employee(
        self, employee_request: EmployeeRequestDto
    ) -> EmployeeResponseDTO:
        """
        Adds a new employee to the system.

        Args:
            employee_request: DTO containing the employee details

        Returns:
            DTO with the created employee data

        Raises:
            ConflictException: If an employee with the same DNI already exists
            NotFoundException: If the position or area does not exist
        """
        existing_employee = await self.repository.exists_by(dni=employee_request.dni)
        if existing_employee:
            raise ConflictException(
                details=f"Employee with DNI {employee_request.dni} already exists",
            )
        existing_position = await self.position_repository.exists_by(
            id=employee_request.cargo_id
        )
        if not existing_position:
            raise NotFoundException(
                details=f"Position with ID {employee_request.cargo_id} does not exist",
            )
        existing_area = await self.area_repository.exists_by(
            id=employee_request.area_id
        )
        if not existing_area:
            raise NotFoundException(
                details=f"Area with ID {employee_request.area_id} does not exist",
            )

        new_employee = Trabajador(
            dni=employee_request.dni,
            nombres=employee_request.nombres,
            apellido_paterno=employee_request.apellido_paterno,
            apellido_materno=employee_request.apellido_materno,
            genero=employee_request.genero.value,
            cargo_id=employee_request.cargo_id,
            area_id=employee_request.area_id,
        )

        created_employee = await self.repository.save(new_employee)

        return EmployeeResponseDTO(
            id=created_employee.id,
            dni=created_employee.dni,
            nombres=created_employee.nombres,
            apellido_paterno=created_employee.apellido_paterno,
            apellido_materno=created_employee.apellido_materno,
            genero=created_employee.genero,
            area_id=created_employee.area_id,
            cargo_id=created_employee.cargo_id,
            created_at=created_employee.created_at,
            updated_at=created_employee.updated_at,
        )

    @handle_exceptions
    async def get_all_employees(self) -> list[EmployeeResponseDTO]:
        """
        Retrieves all employees from the database.

        Returns:
            List of DTOs containing all employees
        """
        employees = await self.repository.get_all()
        return [
            EmployeeResponseDTO(
                id=employee.id,
                dni=employee.dni,
                nombres=employee.nombres,
                apellido_paterno=employee.apellido_paterno,
                apellido_materno=employee.apellido_materno,
                genero=employee.genero,
                area_id=employee.area_id,
                cargo_id=employee.cargo_id,
                created_at=employee.created_at,
                updated_at=employee.updated_at,
            )
            for employee in employees
        ]

    @handle_exceptions
    async def update_employee(
        self, employee_id: int, employee_request: EmployeeRequestDto
    ) -> EmployeeResponseDTO:
        """
        Updates an existing employee.

        Args:
            employee_id: ID of the employee to update
            employee_request: DTO containing the updated employee details

        Returns:
            DTO with the updated employee data

        Raises:
            NotFoundException: If the employee with the given ID doesn't exist
            ConflictException: If another employee with the same DNI already exists
            NotFoundException: If the position or area does not exist
        """
        exists_employee_id = await self.repository.exists_by(id=employee_id)
        if not exists_employee_id:
            raise NotFoundException(
                details=f"Employee with id {employee_id} not found",
            )

        employee = await self.repository.get_by_id(employee_id)

        if employee.dni != employee_request.dni:
            existing_employee = await self.repository.exists_by(
                dni=employee_request.dni
            )
            if existing_employee:
                raise ConflictException(
                    details=f"Employee with DNI {employee_request.dni} already exists",
                )

        existing_position = await self.position_repository.exists_by(
            id=employee_request.cargo_id
        )
        if not existing_position:
            raise NotFoundException(
                details=f"Position with ID {employee_request.cargo_id} does not exist",
            )

        existing_area = await self.area_repository.exists_by(
            id=employee_request.area_id
        )
        if not existing_area:
            raise NotFoundException(
                details=f"Area with ID {employee_request.area_id} does not exist",
            )

        employee.dni = employee_request.dni
        employee.nombres = employee_request.nombres
        employee.apellido_paterno = employee_request.apellido_paterno
        employee.apellido_materno = employee_request.apellido_materno
        employee.genero = employee_request.genero.value
        employee.cargo_id = employee_request.cargo_id
        employee.area_id = employee_request.area_id
        employee.updated_at = datetime.now()

        updated_employee = await self.repository.save(employee)

        return EmployeeResponseDTO(
            id=updated_employee.id,
            dni=updated_employee.dni,
            nombres=updated_employee.nombres,
            apellido_paterno=updated_employee.apellido_paterno,
            apellido_materno=updated_employee.apellido_materno,
            genero=updated_employee.genero,
            area_id=updated_employee.area_id,
            cargo_id=updated_employee.cargo_id,
            created_at=updated_employee.created_at,
            updated_at=updated_employee.updated_at,
        )

    @handle_exceptions
    async def delete_employee(self, employee_id: int) -> MessageResponse:
        """
        Deletes an employee by their ID.

        Args:
            employee_id: ID of the employee to delete

        Returns:
            Message response indicating success or failure

        Raises:
            NotFoundException: If the employee with the given ID doesn't exist
        """
        existing_employee_id = await self.repository.exists_by(id=employee_id)
        if not existing_employee_id:
            raise NotFoundException(
                details=f"Employee with id {employee_id} not found",
            )

        response = await self.repository.delete(employee_id)

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

        Args:
            employee_id: ID of the employee to retrieve

        Returns:
            DTO with the employee data

        Raises:
            NotFoundException: If the employee with the given ID doesn't exist
        """
        existing_employee_id = await self.repository.exists_by(id=employee_id)
        if not existing_employee_id:
            raise NotFoundException(
                details=f"Employee with id {employee_id} not found",
            )

        employee = await self.repository.get_by_id(employee_id)

        return EmployeeResponseDTO(
            id=employee.id,
            dni=employee.dni,
            nombres=employee.nombres,
            apellido_paterno=employee.apellido_paterno,
            apellido_materno=employee.apellido_materno,
            genero=employee.genero,
            area_id=employee.area_id,
            cargo_id=employee.cargo_id,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
        )

    @handle_exceptions
    async def get_employees_paginated(self, page: int, size: int) -> EmployeePage:
        """
        Retrieves a paginated list of employees.

        Args:
            page: Page number to retrieve
            size: Number of items per page

        Returns:
            Paginated employees with metadata

        Raises:
            BadRequestException: If page or size parameters are invalid
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

        page_result = await self.repository.get_pageable(page, size)
        employee_response = [
            EmployeeResponseDTO(**employe_dict) for employe_dict in page_result.data
        ]
        return EmployeePage(
            data=employee_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> EmployeePage:
        """
        Searches for employees matching the given search criteria.

        Args:
            page: Page number to retrieve
            size: Number of items per page
            search_term: Dictionary with field names and search terms

        Returns:
            Paginated employees matching the search criteria

        Raises:
            BadRequestException: If page or size parameters are invalid
            NotFoundException: If no employees match the search criteria
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
            "nombres": search_term,
            "apellido_paterno": search_term,
            "apellido_materno": search_term,
            "dni": search_term if search_term and search_term.isdigit() else None,
        }

        page_result = await self.repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details="No employees found with the provided search criteria",
            )

        employee_response = [
            EmployeeResponseDTO(**employe_dict) for employe_dict in page_result.data
        ]

        return EmployeePage(
            data=employee_response,
            meta=page_result.meta,
        )
