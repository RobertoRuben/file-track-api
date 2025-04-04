from datetime import datetime
from src.app.model.entity import Role
from src.app.dto.request import RoleRequestDTO
from src.app.dto.response import RolePage, RoleResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IRoleRepository
from src.app.service.interfaces import IRoleService


class RoleServiceImpl(IRoleService):
    """
    Implementation of the role service interface.

    Provides business logic for role operations including creating,
    updating, deleting, and querying roles.

    :ivar role_repository: Repository for role data access operations
    """

    def __init__(self, role_repository: IRoleRepository):
        """
        Initialize the role service with a repository.

        :param role_repository: The role repository implementation
        """
        self.role_repository = role_repository

    @handle_exceptions
    async def add_role(self, role_request: RoleRequestDTO) -> RoleResponseDTO:
        """
        Create a new role.

        Validates that the role name does not already exist before creating the new entry.

        :param role_request: DTO containing the role data
        :return: A DTO containing the created role details
        :raises ConflictException: If a role with the same name already exists
        """
        exists_role = await self.role_repository.exists_by(name=role_request.name)
        if exists_role:
            raise ConflictException(
                details=f"Role with name {role_request.name} already exists.",
            )

        new_role = Role(
            name=role_request.name,
        )

        created_role = await self.role_repository.save(new_role)

        return RoleResponseDTO(
            id=created_role.id,
            name=created_role.name,
            created_at=created_role.created_at,
            updated_at=created_role.updated_at,
        )

    @handle_exceptions
    async def get_all_roles(self) -> list[RoleResponseDTO]:
        """
        Retrieve all roles.

        :return: A list of DTOs containing all roles
        """
        roles = await self.role_repository.get_all()
        return [
            RoleResponseDTO(
                id=role.id,
                name=role.name,
                created_at=role.created_at,
                updated_at=role.updated_at,
            )
            for role in roles
        ]

    @handle_exceptions
    async def update_role(
        self, role_id: int, role_request: RoleRequestDTO
    ) -> RoleResponseDTO:
        """
        Update an existing role.

        Validates that the role exists and that the new name is not already taken.

        :param role_id: ID of the role to update
        :param role_request: DTO containing the updated data
        :return: A DTO containing the updated role details
        :raises NotFoundException: If the role with the given ID does not exist
        :raises ConflictException: If another role with the new name already exists
        """
        exists_role_id = await self.role_repository.exists_by(id=role_id)
        if not exists_role_id:
            raise NotFoundException(
                details=f"Role with id {role_id} not found.",
            )
        role = await self.role_repository.get_by_id(role_id)

        if role.name != role_request.name:
            name_exists = await self.role_repository.exists_by(name=role_request.name)
            if name_exists:
                raise ConflictException(
                    details=f"Role with name {role_request.name} already exists.",
                )

        role.name = role_request.name
        role.updated_at = datetime.now()

        updated_role = await self.role_repository.save(role)

        return RoleResponseDTO(
            id=updated_role.id,
            name=updated_role.name,
            created_at=updated_role.created_at,
            updated_at=updated_role.updated_at,
        )

    @handle_exceptions
    async def delete_role(self, role_id: int) -> MessageResponse:
        """
        Delete a role by its ID.

        :param role_id: ID of the role to delete
        :return: A message response indicating success or failure
        :raises NotFoundException: If the role with the given ID does not exist
        """
        exists_role_id = await self.role_repository.exists_by(id=role_id)
        if not exists_role_id:
            raise NotFoundException(
                details=f"Role with ID {role_id} not found.",
            )
        response = await self.role_repository.delete(role_id)
        if response is True:
            return MessageResponse(
                message="Role deleted successfully.",
                success=True,
                details=f"Role with ID {role_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete role.",
                success=False,
                details=f"Role with ID {role_id} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def get_role_by_id(self, role_id: int) -> RoleResponseDTO:
        """
        Retrieve a role by its ID.

        :param role_id: ID of the role to retrieve
        :return: A DTO containing the role details
        :raises NotFoundException: If the role with the given ID does not exist
        """
        exists_role_id = await self.role_repository.exists_by(id=role_id)
        if not exists_role_id:
            raise NotFoundException(
                details=f"Role with ID {role_id} not found.",
            )
        role = await self.role_repository.get_by_id(role_id)
        return RoleResponseDTO(
            id=role.id,
            name=role.name,
            created_at=role.created_at,
            updated_at=role.updated_at,
        )

    @handle_exceptions
    async def get_paginated_roles(self, page: int, size: int) -> RolePage:
        """
        Retrieve a paginated list of roles.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :return: A page object containing roles and pagination metadata
        :raises BadRequestException: If page or size values are invalid
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

        page_result = await self.role_repository.get_pageable(page=page, size=size)
        role_response = [RoleResponseDTO(**role.__dict__) for role in page_result.data]

        return RolePage(
            data=role_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> RolePage:
        """
        Search for roles with name filtering and pagination.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :param search_term: Term to search for in role names
        :return: A page object containing the filtered roles and pagination metadata
        :raises BadRequestException: If page or size values are invalid
        :raises NotFoundException: If no roles match the search criteria
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

        search_dict = {"name": search_term}

        page_result = await self.role_repository.find(page, size, search_dict)

        if page_result.data is None:
            raise NotFoundException(
                details=f"No roles found with the search term {search_term}.",
            )

        role_response = [RoleResponseDTO(**role.__dict__) for role in page_result.data]

        return RolePage(
            data=role_response,
            meta=page_result.meta,
        )
