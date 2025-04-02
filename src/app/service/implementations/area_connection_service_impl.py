from datetime import datetime
from src.app.model.entity import ComunicacionArea
from src.app.dto.request import AreaConnectionRequestDto
from src.app.dto.response import AreaConnectionPage, AreaConnectionResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IAreaConnectionRepository
from src.app.repository.interfaces import IAreaRepository
from src.app.service.interfaces import IAreaConnectionService


class AreaConnectionServiceImpl(IAreaConnectionService):
    """
    Implementation of the AreaConnectionService interface.
    Handles the business logic for area connections.
    """

    def __init__(
        self,
        repository: IAreaConnectionRepository,
        area_repository: IAreaRepository,
    ):
        """
        Initializes the AreaConnectionServiceImpl with the given repositories.

        Args:
            repository (IAreaConnectionRepository): The area connection repository.
            area_repository (IAreaRepository): The area repository.
        """
        self.repository = repository
        self.area_repository = area_repository

    @handle_exceptions
    async def add_area_connection(
        self, area_connection_request: AreaConnectionRequestDto
    ) -> AreaConnectionResponseDTO:
        """
        Adds a new area connection.

        Args:
            area_connection_request (AreaConnectionRequestDto): The request DTO containing area connection details.

        Returns:
            AreaConnectionResponseDTO: The response DTO containing the created area connection details.

        Raises:
            BadRequestException: If the area connection already exists.
            NotFoundException: If the source or destination area does not exist.
        """
        existing_origin_area_id = await self.area_repository.exists_by(
            id=area_connection_request.area_origen_id
        )
        if not existing_origin_area_id:
            raise NotFoundException(
                details=f"Area with ID {area_connection_request.area_origen_id} not found.",
            )
        existing_destination_area_id = await self.area_repository.exists_by(
            id=area_connection_request.area_destino_id
        )
        if not existing_destination_area_id:
            raise NotFoundException(
                details=f"Area with ID {area_connection_request.area_destino_id} not found.",
            )
        existing_area_connection = await self.repository.exists_by(
            area_origen_id=area_connection_request.area_origen_id,
            area_destino_id=area_connection_request.area_destino_id,
        )
        if existing_area_connection:
            raise ConflictException(
                details=f"Area connection already exists between area {area_connection_request.area_origen_id} and "
                f"area {area_connection_request.area_destino_id}.",
            )

        new_area_connection = ComunicacionArea(
            area_origen_id=area_connection_request.area_origen_id,
            area_destino_id=area_connection_request.area_destino_id,
        )

        created_area_connection = await self.repository.save(new_area_connection)

        return AreaConnectionResponseDTO(
            id=created_area_connection.id,
            area_origen_id=created_area_connection.area_origen_id,
            area_destino_id=created_area_connection.area_destino_id,
            created_at=created_area_connection.created_at,
            updated_at=created_area_connection.updated_at,
        )

    @handle_exceptions
    async def get_all_area_connections(self) -> list[AreaConnectionResponseDTO]:
        """
        Retrieves all area connections.

        Returns:
            list[AreaConnectionResponseDTO]: A list of response DTOs containing area connection details.
        """
        area_connections = await self.repository.get_all()
        return [
            AreaConnectionResponseDTO(
                id=connection.id,
                area_origen_id=connection.area_origen_id,
                area_destino_id=connection.area_destino_id,
            )
            for connection in area_connections
        ]

    @handle_exceptions
    async def update_area_connection(
        self, area_connection_id: int, area_connection_request: AreaConnectionRequestDto
    ) -> AreaConnectionResponseDTO:
        """
        Updates an existing area connection.
        Args:
            area_connection_id (int): The ID of the area connection to update.
            area_connection_request (AreaConnectionRequestDto): The request DTO containing updated area connection
            details.
        Returns:
            AreaConnectionResponseDTO: The response DTO containing the updated area connection details.
        Raises:
            NotFoundException: If the area connection does not exist.
            ConflictException: If the area connection already exists or has same source and destination areas.
            BadRequestException: If the area connection already exists.
        """
        if area_connection_id < 0:
            raise BadRequestException(
                message="Invalid area connection ID",
                details="Area connection ID must be greater than or equal to 0.",
            )

        existing_origin_area_id = await self.area_repository.exists_by(
            id=area_connection_request.area_origen_id
        )
        if not existing_origin_area_id:
            raise NotFoundException(
                details=f"Area with ID {area_connection_request.area_origen_id} not found.",
            )
        existing_destination_area_id = await self.area_repository.exists_by(
            id=area_connection_request.area_destino_id
        )
        if not existing_destination_area_id:
            raise NotFoundException(
                details=f"Area with ID {area_connection_request.area_destino_id} not found.",
            )

        existing_area_connection = await self.repository.exists_by(
            area_origen_id=area_connection_request.area_origen_id,
            area_destino_id=area_connection_request.area_destino_id,
        )
        if existing_area_connection:
            raise ConflictException(
                details=f"Area connection already exists between area {area_connection_request.area_origen_id} and "
                f"area {area_connection_request.area_destino_id}.",
            )

        area_connection = await self.repository.get_by_id(area_connection_id)

        area_connection.area_origen_id = area_connection_request.area_origen_id
        area_connection.area_destino_id = area_connection_request.area_destino_id
        area_connection.updated_at = datetime.now()

        updated_area_connection = await self.repository.save(area_connection)

        return AreaConnectionResponseDTO(
            id=updated_area_connection.id,
            area_origen_id=updated_area_connection.area_origen_id,
            area_destino_id=updated_area_connection.area_destino_id,
            created_at=updated_area_connection.created_at,
            updated_at=updated_area_connection.updated_at,
        )

    @handle_exceptions
    async def delete_area_connection(self, area_connection_id: int) -> MessageResponse:
        """
        Deletes an area connection by its ID.

        Args:
            area_connection_id (int): The ID of the area connection to delete.

        Returns:
            MessageResponse: A message indicating the result of the operation.

        Raises:
            NotFoundException: If the area connection with the given ID doesn't exist.
        """
        existing_area_connection = await self.repository.exists_by(
            id=area_connection_id
        )
        if not existing_area_connection:
            raise NotFoundException(
                details=f"Area connection with ID {area_connection_id} not found.",
            )
        response = await self.repository.delete(area_connection_id)
        if response is True:
            return MessageResponse(
                message="Area connection deleted successfully.",
                success=True,
                details=f"Area connection with ID {area_connection_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete area connection.",
                success=False,
                details=f"Failed to delete area connection with ID {area_connection_id}.",
                status_code=500,
            )

    @handle_exceptions
    async def get_area_connection_by_id(
        self, area_connection_id: int
    ) -> AreaConnectionResponseDTO:
        """
        Retrieves an area connection by its ID.

        Args:
            area_connection_id (int): The ID of the area connection to retrieve.

        Returns:
            AreaConnectionResponseDTO: The response DTO containing area connection details.

        Raises:
            NotFoundException: If the area connection with the given ID doesn't exist.
        """
        if area_connection_id < 0:
            raise BadRequestException(
                message="Invalid area connection ID",
                details="Area connection ID must be greater than or equal to 0.",
            )
        existing_connection = await self.repository.exists_by(id=area_connection_id)
        if not existing_connection:
            raise NotFoundException(
                details=f"Area connection with ID {area_connection_id} not found.",
            )

        connection = await self.repository.get_by_id(area_connection_id)

        return AreaConnectionResponseDTO(
            id=connection.id,
            area_origen_id=connection.area_origen_id,
            area_destino_id=connection.area_destino_id,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )

    @handle_exceptions
    async def get_paginated_area_connections(
        self, page: int, size: int
    ) -> AreaConnectionPage:
        """
        Retrieves a paginated list of area connections.

        Args:
            page (int): The page number (starts at 1).
            size (int): The size of each page.

        Returns:
            AreaConnectionPage: A paginated response containing area connections.

        Raises:
            BadRequestException: If page or size parameters are invalid.
        """
        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        page_result = await self.repository.get_pageable(page, size)
        area_connection_response = [
            AreaConnectionResponseDTO(**connection_dict)
            for connection_dict in page_result.data
        ]

        return AreaConnectionPage(
            data=area_connection_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> AreaConnectionPage:
        """
        Searches for area connections based on search criteria.

        Args:
            page (int): The page number (starts at 1).
            size (int): The size of each page.
            search_term (str): The term to search for.

        Returns:
            AreaConnectionPage: A paginated response containing matching area connections.

        Raises:
            BadRequestException: If page or size parameters are invalid.
            NotFoundException: If no area connections match the search criteria.
        """
        if page < 1 or size < 1:
            raise BadRequestException(
                message="Invalid pagination parameters",
                details="Page and size must be greater than 0.",
            )

        search_dict = {
            "area_origen_id": search_term,
            "area_destino_id": search_term,
            "area_origen_nombre": search_term,
            "area_destino_nombre": search_term,
        }

        page_result = await self.repository.find(page, size, search_dict)
        if not page_result.data:
            raise NotFoundException(
                details=f"No area connections found matching the search term {search_term}.",
            )

        area_connection_response = [
            AreaConnectionResponseDTO(**connection_dict)
            for connection_dict in page_result.data
        ]

        return AreaConnectionPage(
            data=area_connection_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def get_connections_by_area_origen_id(
        self, area_origen_id: int
    ) -> list[AreaConnectionResponseDTO]:
        """
        Retrieves area connections by area origin ID.

        Args:
            area_origen_id (int): The ID of the area origin.

        Returns:
            list[AreaConnectionResponseDTO]: A list of response DTOs containing area connection details.
        """
        if area_origen_id < 0:
            raise BadRequestException(
                message="Invalid area origin ID",
                details="Area origin ID must be greater than or equal to 0.",
            )
        existing_area = await self.area_repository.exists_by(id=area_origen_id)
        if not existing_area:
            raise NotFoundException(
                details=f"Area with ID {area_origen_id} not found.",
            )
        connections = await self.repository.get_connections_by_area_origen_id(
            area_origen_id
        )
        return [
            AreaConnectionResponseDTO(
                id=connection.id,
                area_origen_id=connection.area_origen_id,
                area_destino_id=connection.area_destino_id,
                created_at=connection.created_at,
                updated_at=connection.updated_at,
            )
            for connection in connections
        ]
