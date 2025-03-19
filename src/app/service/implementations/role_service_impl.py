from datetime import datetime
from src.app.model.entity import Rol
from src.app.dto.request import RoleRequestDTO
from src.app.dto.response import RolePage, RoleResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IRolRepository
from src.app.service.interfaces import IRoleService


class RoleServiceImpl(IRoleService):
    """
    Implementation of the role service interface.

    Provides business logic for role operations including creating,
    updating, deleting, and querying roles.
    """

    def __init__(self, repository: IRolRepository):
        """
        Initialize the role service with a repository.

        Args:
            repository: The role repository implementation
        """
        self.repository = repository

    @handle_exceptions
    async def add_role(self, role_request: RoleRequestDTO) -> RoleResponseDTO:
        """
        Create a new role.

        Validates that the role name does not already exist before creating the new entry.

        Args:
            role_request: DTO containing the role data

        Returns:
            A DTO containing the created role details

        Raises:
            ConflictException: If a role with the same name already exists
        """
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
        """
        Retrieve all roles.

        Returns:
            A list of DTOs containing all roles
        """
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
        """
        Update an existing role.

        Validates that the role exists and that the new name is not already taken.

        Args:
            role_id: ID of the role to update
            role_request: DTO containing the updated data

        Returns:
            A DTO containing the updated role details

        Raises:
            NotFoundException: If the role with the given ID does not exist
            ConflictException: If another role with the new name already exists
        """
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
        """
        Delete a role by its ID.

        Args:
            role_id: ID of the role to delete

        Returns:
            A message response indicating success or failure

        Raises:
            NotFoundException: If the role with the given ID does not exist
        """
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
        """
        Retrieve a role by its ID.

        Args:
            role_id: ID of the role to retrieve

        Returns:
            A DTO containing the role details

        Raises:
            NotFoundException: If the role with the given ID does not exist
        """
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
        """
        Retrieve a paginated list of roles.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page

        Returns:
            A page object containing roles and pagination metadata

        Raises:
            BadRequestException: If page or size values are invalid
        """
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
        """
        Search for roles with name filtering and pagination.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page
            search_term: Term to search for in role names

        Returns:
            A page object containing the filtered roles and pagination metadata

        Raises:
            BadRequestException: If page or size values are invalid
            NotFoundException: If no roles match the search criteria
        """
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