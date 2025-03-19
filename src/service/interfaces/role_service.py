from abc import ABC, abstractmethod
from src.dto.request import RoleRequestDTO
from src.dto.response import RoleResponseDTO, RolePage
from src.schema import MessageResponse

class IRoleService(ABC):
    """
    Interface for role service operations.
    Defines the contract for role-related business logic.
    """

    @abstractmethod
    async def add_role(self, role_request: RoleRequestDTO) -> RoleResponseDTO:
        """
        Add a new role.

        Args:
            role_request: The data transfer object containing role details.

        Returns:
            The created role as a RoleResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_roles(self) -> list[RoleResponseDTO]:
        """
        Retrieve all roles.

        Returns:
            A list of RoleResponseDTO objects representing all roles.
        """
        pass

    @abstractmethod
    async def update_role(self, role_id: int, role_request: RoleRequestDTO) -> RoleResponseDTO:
        """
        Update an existing role.

        Args:
            role_id: The ID of the role to update.
            role_request: The data transfer object containing updated role details.

        Returns:
            The updated role as a RoleResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_role(self, role_id: int) -> MessageResponse:
        """
        Delete a role by its ID.

        Args:
            role_id: The ID of the role to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_role_by_id(self, role_id: int) -> RoleResponseDTO:
        """
        Retrieve a role by its ID.

        Args:
            role_id: The ID of the role to retrieve.

        Returns:
            The role as a RoleResponseDTO.
        """
        pass

    @abstractmethod
    async def get_paginated_roles(self, page: int, size: int) -> RolePage:
        """
        Retrieve a paginated list of roles.

        Args:
            page: The page number to retrieve.
            size: The number of roles per page.

        Returns:
            A RolePage object containing the paginated roles.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> RolePage:
        """
        Find roles based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of roles per page.
            search_term: The term to search for in role names.

        Returns:
            A RolePage object containing the roles that match the search criteria.
        """
        pass