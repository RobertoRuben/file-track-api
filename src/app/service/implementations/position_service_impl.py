from datetime import datetime
from src.app.model.entity import Position
from src.app.dto.request import PositionRequestDTO
from src.app.dto.response import PositionPage, PositionResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IPositionRepository
from src.app.service.interfaces import IPositionService


class PositionServiceImpl(IPositionService):
    """
    Implementation of the Position Service interface.
    Handles business logic for position-related operations.
    """

    def __init__(self, position_repository: IPositionRepository):
        """
        Initializes the Position Service with a repository.

        :param position_repository: The repository for position data access
        """
        self.position_repository = position_repository

    @handle_exceptions
    async def add_position(
        self, position_request: PositionRequestDTO
    ) -> PositionResponseDTO:
        """
        Adds a new position to the system.

        :param position_request: DTO containing the position details
        :return: DTO with the created position data

        :raises ConflictException: If a position with the same name already exists
        """
        existing_position = await self.position_repository.exists_by(
            name=position_request.name
        )
        if existing_position:
            raise ConflictException(
                details=f"Position with name {position_request.name} already exists",
            )

        new_position = Position(
            name=position_request.name,
        )

        created_position = await self.position_repository.save(new_position)

        return PositionResponseDTO(
            id=created_position.id,
            name=created_position.name,
            created_at=created_position.created_at,
            updated_at=created_position.updated_at,
        )

    @handle_exceptions
    async def get_all_positions(self) -> list[PositionResponseDTO]:
        """
        Retrieves all positions from the database.

        :return: List of DTOs containing all positions
        """
        positions = await self.position_repository.get_all()
        return [
            PositionResponseDTO(
                id=position.id,
                name=position.name,
                created_at=position.created_at,
                updated_at=position.updated_at,
            )
            for position in positions
        ]

    @handle_exceptions
    async def update_position(
        self, position_id: int, position_request: PositionRequestDTO
    ) -> PositionResponseDTO:
        """
        Updates an existing position.

        :param position_id: ID of the position to update
        :param position_request: DTO containing the updated position details
        :return: DTO with the updated position data

        :raises NotFoundException: If the position with the given ID doesn't exist
        :raises ConflictException: If another position with the same name already exists
        """
        exists_position_id = await self.position_repository.exists_by(id=position_id)
        if not exists_position_id:
            raise NotFoundException(
                details=f"Position with id {position_id} not found",
            )
        position = await self.position_repository.get_by_id(position_id)

        if position.name != position_request.name:
            existing_position = await self.position_repository.exists_by(
                name=position_request.name
            )
            if existing_position:
                raise ConflictException(
                    details=f"Position with name {position_request.name} already exists",
                )

        position.name = position_request.name
        position.updated_at = datetime.now()

        updated_position = await self.position_repository.save(position)

        return PositionResponseDTO(
            id=updated_position.id,
            name=updated_position.name,
            created_at=updated_position.created_at,
            updated_at=updated_position.updated_at,
        )

    @handle_exceptions
    async def delete_position(self, position_id: int) -> MessageResponse:
        """
        Deletes a position by its ID.

        :param position_id: ID of the position to delete
        :return: Message response indicating success or failure

        :raises NotFoundException: If the position with the given ID doesn't exist
        """
        existing_position_id = await self.position_repository.exists_by(id=position_id)
        if not existing_position_id:
            raise NotFoundException(
                details=f"Position with id {position_id} not found",
            )
        response = await self.position_repository.delete(position_id)
        if response is True:
            return MessageResponse(
                message="Position deleted successfully.",
                success=True,
                details=f"Position with id {position_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete position.",
                success=False,
                details=f"Position with id {position_id} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def get_position_by_id(self, position_id: int) -> PositionResponseDTO:
        """
        Retrieves a position by its ID.

        :param position_id: ID of the position to retrieve
        :return: DTO with the position data

        :raises NotFoundException: If the position with the given ID doesn't exist
        """
        existing_position_id = await self.position_repository.exists_by(id=position_id)
        if not existing_position_id:
            raise NotFoundException(
                details=f"Position with id {position_id} not found",
            )
        position = await self.position_repository.get_by_id(position_id)
        return PositionResponseDTO(
            id=position.id,
            name=position.name,
            created_at=position.created_at,
            updated_at=position.updated_at,
        )

    @handle_exceptions
    async def get_positions_paginated(self, page: int, size: int) -> PositionPage:
        """
        Retrieves a paginated list of positions.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :return: Paginated positions with metadata

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

        page_result = await self.position_repository.get_pageable(page, size)
        position_response = [
            PositionResponseDTO(**position.__dict__) for position in page_result.data
        ]

        return PositionPage(
            data=position_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> PositionPage:
        """
        Searches for positions matching the given search term.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :param search_term: Term to search for in position names
        :return: Paginated positions matching the search criteria

        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no positions match the search criteria
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

        search_dict = {"name": search_term}

        page_result = await self.position_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details=f"No positions found with the search term {search_term}",
            )

        position_response = [
            PositionResponseDTO(**position.__dict__) for position in page_result.data
        ]

        return PositionPage(
            data=position_response,
            meta=page_result.meta,
        )
