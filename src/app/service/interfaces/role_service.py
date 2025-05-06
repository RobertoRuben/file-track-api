from abc import ABC, abstractmethod
from src.app.dto.request import RoleRequestDTO
from src.app.dto.response import RoleResponseDTO, RolePage
from src.app.schema import MessageResponse


class IRoleService(ABC):
    """
    Interface for role service operations.
    Defines the contract for role-related business logic.
    """

    @abstractmethod
    async def add_role(self, role_request: RoleRequestDTO) -> RoleResponseDTO:
        """
        Add a new role.

        :param role_request: The data transfer object containing role details
        :return: The created role as a RoleResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_roles(self) -> list[RoleResponseDTO]:
        """
        Retrieve all roles.

        :return: A list of RoleResponseDTO objects representing all roles
        """
        pass

    @abstractmethod
    async def update_role(
        self, role_id: int, role_request: RoleRequestDTO
    ) -> RoleResponseDTO:
        """
        Update an existing role.

        :param role_id: The ID of the role to update
        :param role_request: The data transfer object containing updated role details
        :return: The updated role as a RoleResponseDTO
        """
        pass

    @abstractmethod
    async def delete_role(self, role_id: int) -> MessageResponse:
        """
        Delete a role by its ID.

        :param role_id: The ID of the role to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_role_by_id(self, role_id: int) -> RoleResponseDTO:
        """
        Retrieve a role by its ID.

        :param role_id: The ID of the role to retrieve
        :return: The role as a RoleResponseDTO
        """
        pass

    @abstractmethod
    async def get_paginated_roles(self, page: int, size: int) -> RolePage:
        """
        Retrieve a paginated list of roles.

        :param page: The page number to retrieve
        :param size: The number of roles per page
        :return: A RolePage object containing the paginated roles
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> RolePage:
        """
        Find roles based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of roles per page
        :param search_term: The term to search for in role names
        :return: A RolePage object containing the roles that match the search criteria
        """
        pass

    @abstractmethod
    async def delete_roles_by_ids(self, role_ids: list[int]) -> MessageResponse:
        """
        Delete multiple roles by their IDs.

        :param role_ids: List of role IDs to delete
        :return: Message with the number of deleted roles
        """
        pass

    @abstractmethod
    async def export_roles_to_excel(self, role_ids: list[int]) -> bytes:
        """
        Export roles to Excel format by their IDs.

        :param role_ids: List of role IDs to export
        :return: Excel file as bytes
        """
        pass
