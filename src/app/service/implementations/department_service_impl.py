from datetime import datetime
from src.app.model.entity import Area
from src.app.dto.request import DepartmentRequestDTO
from src.app.dto.response import DepartmentPage, DepartmentResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IAreaRepository
from src.app.service.interfaces import IDepartmentService

class DepartmentServiceImpl(IDepartmentService):

    def __init__(self, repository: IAreaRepository):
        self.repository = repository

    @handle_exceptions
    async def add_department(self, department_request: DepartmentRequestDTO) -> DepartmentResponseDTO:
        existing_department = await self.repository.exists_by(nombre=department_request.nombre)
        if existing_department:
            raise ConflictException(
                details=f"Department with name {department_request.nombre} already exists",
            )

        new_department = Area(
            nombre = department_request.nombre,
        )

        created_department = await self.repository.save(new_department)

        return DepartmentResponseDTO(
            id=created_department.id,
            nombre=created_department.nombre,
            created_at=created_department.created_at,
            updated_at=created_department.updated_at,
        )

    @handle_exceptions
    async def get_all_departments(self) -> list[DepartmentResponseDTO]:
        departments = await self.repository.get_all()
        return [
            DepartmentResponseDTO(
                id=department.id,
                nombre=department.nombre,
                created_at=department.created_at,
                updated_at=department.updated_at
            )
            for department in departments
        ]

    @handle_exceptions
    async def update_department(self, department_id: int, department_request: DepartmentRequestDTO) -> DepartmentResponseDTO:
        exists_department_id = await self.repository.exists_by(id=department_id)
        if not exists_department_id:
            raise NotFoundException(
                details=f"Department with id {department_id} not found",
            )
        department = await self.repository.get_by_id(department_id)

        if department.nombre != department_request.nombre:
            existing_department = await self.repository.exists_by(nombre=department_request.nombre)
            if existing_department:
                raise ConflictException(
                    details=f"Department with name {department_request.nombre} already exists",
                )

        department.nombre = department_request.nombre
        department.updated_at = datetime.now()

        updated_department = await self.repository.save(department)

        return DepartmentResponseDTO(
            id=updated_department.id,
            nombre=updated_department.nombre,
            created_at=updated_department.created_at,
            updated_at=updated_department.updated_at,
        )

    @handle_exceptions
    async def delete_department(self, department_id: int) -> MessageResponse:
        existing_department_id = await self.repository.exists_by(id=department_id)
        if not existing_department_id:
            raise NotFoundException(
                details=f"Department with id {department_id} not found",
            )
        response = await self.repository.delete(department_id)
        if response is True:
            return MessageResponse(
                message="Department deleted successfully.",
                success=True,
                details=f"Department with id {department_id} deleted successfully.",
                status_code=200
            )
        else:
            return MessageResponse(
                message="Failed to delete department.",
                success=False,
                details=f"Department with id {department_id} could not be deleted.",
                status_code=500
            )

    @handle_exceptions
    async def get_department_by_id(self, department_id: int) -> DepartmentResponseDTO:
        existing_department_id = await self.repository.exists_by(id=department_id)
        if not existing_department_id:
            raise NotFoundException(
                details=f"Department with id {department_id} not found",
            )
        department = await self.repository.get_by_id(department_id)
        return DepartmentResponseDTO(
            id=department.id,
            nombre=department.nombre,
            created_at=department.created_at,
            updated_at=department.updated_at
        )

    @handle_exceptions
    async def get_departments_paginated(self, page: int, size: int) -> DepartmentPage:
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
        department_response = [
            DepartmentResponseDTO(**department.__dict__) for department in page_result.data
        ]

        return DepartmentPage(
            data=department_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> DepartmentPage:
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
            "nombre": search_term
        }

        page_result = await self.repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details=f"No departments found with the search term {search_term}",
            )

        department_response = [DepartmentResponseDTO(**department.__dict__) for department in page_result.data]

        return DepartmentPage(
            data=department_response,
            meta=page_result.meta,
        )