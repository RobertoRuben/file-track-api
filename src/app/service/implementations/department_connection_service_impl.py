from datetime import datetime
from src.app.model.entity import DepartmentConnection
from src.app.dto.request import DepartmentConnectionRequestDTO
from src.app.dto.response import (
    DepartmentConnectionPage,
    DepartmentConnectionResponseDTO,
    CurrentUserResponseDTO,
)
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IDepartmentConnectionRepository
from src.app.repository.interfaces import IDepartmentRepository
from src.app.service.interfaces import IDepartmentConnectionService
from src.app.exception.constants import ErrorTypes, ErrorTitles


class DepartmentConnectionServiceImpl(IDepartmentConnectionService):
    """
    Implementation of the DepartmentConnectionService interface.
    Handles the business logic for department connections.

    :ivar department_connection_repository: Repository for department connection operations
    :ivar department_repository: Repository for department operations
    """

    def __init__(
        self,
        department_connection_repository: IDepartmentConnectionRepository,
        department_repository: IDepartmentRepository,
    ):
        """
        Initializes the DepartmentConnectionServiceImpl with the given repositories.

        :param department_connection_repository: The department connection repository
        :param department_repository: The department repository
        """
        self.department_connection_repository = department_connection_repository
        self.department_repository = department_repository

    @handle_exceptions
    async def add_department_connection(
        self, department_connection_request: DepartmentConnectionRequestDTO
    ) -> DepartmentConnectionResponseDTO:
        """
        Adds a new department connection.

        :param department_connection_request: The request DTO containing department connection details
        :return: The response DTO containing the created department connection details
        :raises BadRequestException: If the department connection already exists
        :raises NotFoundException: If the source or target department does not exist
        """
        existing_source_department = await self.department_repository.exists_by(
            id=department_connection_request.source_department_id
        )
        if not existing_source_department:
            raise NotFoundException(
                message="Source department not found",
                details=f"Department with ID {department_connection_request.source_department_id} not found.",
            )
        existing_target_department = await self.department_repository.exists_by(
            id=department_connection_request.target_department_id
        )
        if not existing_target_department:
            raise NotFoundException(
                message="Target department not found",
                details=f"Department with ID {department_connection_request.target_department_id} not found.",
            )
        existing_connection = await self.department_connection_repository.exists_by(
            source_department_id=department_connection_request.source_department_id,
            target_department_id=department_connection_request.target_department_id,
        )
        if existing_connection:
            raise ConflictException(
                message="Department connection already exists",
                details=f"Department connection already exists between department {department_connection_request.source_department_id} and department {department_connection_request.target_department_id}.",
            )

        new_connection = DepartmentConnection(
            source_department_id=department_connection_request.source_department_id,
            target_department_id=department_connection_request.target_department_id,
        )

        created_connection = await self.department_connection_repository.save(
            new_connection
        )

        return DepartmentConnectionResponseDTO(
            id=created_connection.id,
            source_department_id=created_connection.source_department_id,
            target_department_id=created_connection.target_department_id,
            created_at=created_connection.created_at,
            updated_at=created_connection.updated_at,
        )

    @handle_exceptions
    async def get_all_department_connections(
        self,
    ) -> list[DepartmentConnectionResponseDTO]:
        """
        Retrieves all department connections.

        :return: A list of response DTOs containing department connection details
        """
        connections = await self.department_connection_repository.get_all()
        return [
            DepartmentConnectionResponseDTO(
                id=connection.id,
                source_department_id=connection.source_department_id,
                target_department_id=connection.target_department_id,
            )
            for connection in connections
        ]

    @handle_exceptions
    async def update_department_connection(
        self,
        department_connection_id: int,
        department_connection_request: DepartmentConnectionRequestDTO,
    ) -> DepartmentConnectionResponseDTO:
        """
        Updates an existing department connection.

        :param department_connection_id: The ID of the department connection to update
        :param department_connection_request: The request DTO containing updated connection details
        :return: The response DTO containing the updated department connection details
        :raises NotFoundException: If the department connection does not exist
        :raises ConflictException: If the updated connection already exists or has same source and target departments
        :raises BadRequestException: If the department connection already exists
        """
        if department_connection_id < 0:
            raise BadRequestException(
                message="Invalid department connection ID",
                details="Department connection ID must be greater than or equal to 0.",
            )

        existing_source_department = await self.department_repository.exists_by(
            id=department_connection_request.source_department_id
        )
        if not existing_source_department:
            raise NotFoundException(
                message="Source department not found",
                details=f"Department with ID {department_connection_request.source_department_id} not found.",
            )
        existing_target_department = await self.department_repository.exists_by(
            id=department_connection_request.target_department_id
        )
        if not existing_target_department:
            raise NotFoundException(
                message="Target department not found",
                details=f"Department with ID {department_connection_request.target_department_id} not found.",
            )

        existing_connection = await self.department_connection_repository.exists_by(
            source_department_id=department_connection_request.source_department_id,
            target_department_id=department_connection_request.target_department_id,
        )
        if existing_connection:
            raise ConflictException(
                message="Department connection already exists",
                details=f"Department connection already exists between department {department_connection_request.source_department_id} and department {department_connection_request.target_department_id}.",
            )

        connection = await self.department_connection_repository.get_by_id(
            department_connection_id
        )

        connection.source_department_id = (
            department_connection_request.source_department_id
        )
        connection.target_department_id = (
            department_connection_request.target_department_id
        )
        connection.updated_at = datetime.now()

        updated_connection = await self.department_connection_repository.save(
            connection
        )

        return DepartmentConnectionResponseDTO(
            id=updated_connection.id,
            source_department_id=updated_connection.source_department_id,
            target_department_id=updated_connection.target_department_id,
            created_at=updated_connection.created_at,
            updated_at=updated_connection.updated_at,
        )

    @handle_exceptions
    async def delete_department_connection(
        self, department_connection_id: int
    ) -> MessageResponse:
        """
        Deletes a department connection by its ID.

        :param department_connection_id: The ID of the department connection to delete
        :return: A message indicating the result of the operation
        :raises NotFoundException: If the department connection with the given ID doesn't exist
        """
        existing_connection = await self.department_connection_repository.exists_by(
            id=department_connection_id
        )
        if not existing_connection:
            raise NotFoundException(
                message="Department connection not found",
                details=f"Department connection with ID {department_connection_id} not found.",
            )
        response = await self.department_connection_repository.delete(
            department_connection_id
        )
        if response is True:
            return MessageResponse(
                message="Department connection deleted successfully.",
                success=True,
                details=f"Department connection with ID {department_connection_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete department connection.",
                success=False,
                details=f"Failed to delete department connection with ID {department_connection_id}.",
                status_code=500,
            )

    @handle_exceptions
    async def get_department_connection_by_id(
        self, department_connection_id: int
    ) -> DepartmentConnectionResponseDTO:
        """
        Retrieves a department connection by its ID.

        :param department_connection_id: The ID of the department connection to retrieve
        :return: The response DTO containing department connection details
        :raises NotFoundException: If the department connection with the given ID doesn't exist
        """
        if department_connection_id < 0:
            raise BadRequestException(
                message="Invalid department connection ID",
                details="Department connection ID must be greater than or equal to 0.",
            )
        existing_connection = await self.department_connection_repository.exists_by(
            id=department_connection_id
        )
        if not existing_connection:
            raise NotFoundException(
                message="Department connection not found",
                details=f"Department connection with ID {department_connection_id} not found.",
            )

        connection = await self.department_connection_repository.get_by_id(
            department_connection_id
        )

        return DepartmentConnectionResponseDTO(
            id=connection.id,
            source_department_id=connection.source_department_id,
            target_department_id=connection.target_department_id,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )

    @handle_exceptions
    async def get_paginated_department_connections(
        self, page: int, size: int
    ) -> DepartmentConnectionPage:
        """
        Retrieves a paginated list of department connections.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A paginated response containing department connections
        :raises BadRequestException: If page or size parameters are invalid
        """
        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        page_result = await self.department_connection_repository.get_pageable(
            page, size
        )
        connection_response = [
            DepartmentConnectionResponseDTO(**connection_dict)
            for connection_dict in page_result.data
        ]

        return DepartmentConnectionPage(
            data=connection_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(
        self, page: int, size: int, search_term: str
    ) -> DepartmentConnectionPage:
        """
        Searches for department connections based on search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_term: The term to search for
        :return: A paginated response containing matching department connections
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no department connections match the search criteria
        """
        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        search_dict = {
            "source_department_id": search_term,
            "target_department_id": search_term,
            "source_department_name": search_term,
            "target_department_name": search_term,
        }

        page_result = await self.department_connection_repository.find(
            page, size, search_dict
        )
        if not page_result.data:
            raise NotFoundException(
                message="No results found",
                details=f"No department connections found matching the search term {search_term}.",
            )

        connection_response = [
            DepartmentConnectionResponseDTO(**connection_dict)
            for connection_dict in page_result.data
        ]

        return DepartmentConnectionPage(
            data=connection_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def get_connections_by_source_department_id(
        self, source_department_id: int
    ) -> list[DepartmentConnectionResponseDTO]:
        """
        Retrieves department connections by source department ID.

        :param source_department_id: The ID of the source department
        :return: A list of response DTOs containing department connection details
        :raises BadRequestException: If source_department_id parameter is invalid
        :raises NotFoundException: If the source department doesn't exist
        """
        if source_department_id < 0:
            raise BadRequestException(
                message="Invalid source department ID",
                details="Source department ID must be greater than or equal to 0.",
            )
        existing_department = await self.department_repository.exists_by(
            id=source_department_id
        )
        if not existing_department:
            raise NotFoundException(
                message="Department not found",
                details=f"Department with ID {source_department_id} not found.",
            )
        connections = await self.department_connection_repository.get_connections_by_source_department_id(
            source_department_id
        )
        return [
            DepartmentConnectionResponseDTO(
                id=connection.id,
                source_department_id=connection.source_department_id,
                target_department_id=connection.target_department_id,
                created_at=connection.created_at,
                updated_at=connection.updated_at,
            )
            for connection in connections
        ]

    @handle_exceptions
    async def get_department_connections_by_current_user_department(
        self, current_user: CurrentUserResponseDTO
    ) -> list[DepartmentConnectionResponseDTO]:

        if not current_user.department_id:
            raise NotFoundException(
                message="User department not found",
                details="Current user does not belong to any department.",
            )

        department_id = current_user.department_id

        existing_department = await self.department_repository.exists_by(
            id=department_id
        )
        if not existing_department:
            raise NotFoundException(
                message="Department not found",
                details=f"Department with ID {department_id} not found.",
            )

        connections = await self.department_connection_repository.get_connections_by_source_department_id(
            department_id
        )

        if not connections:
            raise NotFoundException(
                message="No connections found",
                details=f"No department connections found for department ID {department_id}.",
            )

        return [
            DepartmentConnectionResponseDTO(
                id=connection.id,
                source_department_id=connection.source_department_id,
                target_department_id=connection.target_department_id,
                created_at=connection.created_at,
                updated_at=connection.updated_at,
            )
            for connection in connections
        ]
