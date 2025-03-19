from datetime import datetime
from src.model.entity import Rol
from src.dto.request import RoleRequestDTO
from src.dto.response import RolePage, RoleResponseDTO
from src.schema import MessageResponse
from src.exception import BadRequestException, ConflictException, NotFoundException
from src.exception.decorator import handle_exceptions
from src.repository.interfaces import IRolRepository
from src.service.interfaces import IRoleService

class RoleServiceImpl(IRoleService):

    def __init__(self, repository: IRolRepository):
        self.repository = repository

    @handle_exceptions
    async def add_role(self, role_request: RoleRequestDTO) -> RoleResponseDTO:
        exists_role = await self.repository.exists_by(nombre=role_request.nombre)
        if exists_role:
            raise ConflictException(
                details=f"Role with name {role_request.nombre} already exists.",
            )

        new_role = Rol(
            nombre=role_request.nombre,
        )

        created_role = await self.repository.save(new_role)

        return RoleResponseDTO(
            id=created_role.id,
            nombre=created_role.nombre,
            created_at=created_role.created_at,
            updated_at=created_role.updated_at
        )

    @handle_exceptions
    async def get_all_roles(self) -> list[RoleResponseDTO]:
        roles = await self.repository.get_all()
        return [
            RoleResponseDTO(
                id=role.id,
                nombre=role.nombre,
                created_at=role.created_at,
                updated_at=role.updated_at
            )
            for role in roles
        ]

    @handle_exceptions
    async def update_role(self, role_id: int, role_request: RoleRequestDTO) -> RoleResponseDTO:
        exists_role_id = await self.repository.exists_by(id=role_id)
        if not exists_role_id:
            raise NotFoundException(
                details=f"Role with id {role_id} not found.",
            )
        role = await self.repository.get_by_id(role_id)

        if role.nombre != role_request.nombre:
            name_exists = await self.repository.exists_by(nombre=role_request.nombre)
            if name_exists:
                raise ConflictException(
                    details=f"Role with name {role_request.nombre} already exists.",
                )

        role.nombre = role_request.nombre
        role.updated_at = datetime.now()

        updated_role = await self.repository.save(role)

        return RoleResponseDTO(
            id=updated_role.id,
            nombre=updated_role.nombre,
            created_at=updated_role.created_at,
            updated_at=updated_role.updated_at
        )

    @handle_exceptions
    async def delete_role(self, role_id: int) -> MessageResponse:
        exists_role_id = await self.repository.exists_by(id=role_id)
        if not exists_role_id:
            raise NotFoundException(
                details=f"Role with ID {role_id} not found.",
            )
        response = await self.repository.delete(role_id)
        if response is True:
            return MessageResponse(
                message="Role deleted successfully.",
                success=True,
                details=f"Role with ID {role_id} deleted successfully.",
                status_code=200
            )
        else:
            return MessageResponse(
                message="Failed to delete role.",
                success=False,
                details=f"Role with ID {role_id} could not be deleted.",
                status_code=500
            )

    @handle_exceptions
    async def get_role_by_id(self, role_id: int) -> RoleResponseDTO:
        exists_role_id = await self.repository.exists_by(id=role_id)
        if not exists_role_id:
            raise NotFoundException(
                details=f"Role with ID {role_id} not found.",
            )
        role = await self.repository.get_by_id(role_id)
        return RoleResponseDTO(
            id=role.id,
            nombre=role.nombre,
            created_at=role.created_at,
            updated_at=role.updated_at
        )

    @handle_exceptions
    async def get_paginated_roles(self, page: int, size: int) -> RolePage:
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid size number",
                details="Size number must be greater than 0.",
            )

        page_result = await self.repository.get_pageable(page=page, size=size)
        role_response = [RoleResponseDTO(**role.__dict__) for role in page_result.data]

        return RolePage(
            data=role_response,
            meta=page_result.meta,
        )


    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> RolePage:
        if page < 1:
            raise BadRequestException(
                message="Invalid page number",
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid size number",
                details="Size number must be greater than 0.",
            )

        search_dict = {
            "nombre": search_term
        }

        page_result = await self.repository.find(page, size, search_dict)

        if page_result.data is None:
            raise NotFoundException(
                details=f"No roles found with the search term {search_term}.",
            )

        role_response = [RoleResponseDTO(**role.__dict__) for role in page_result.data]

        return RolePage(
            data=role_response,
            meta=page_result.meta,
        )