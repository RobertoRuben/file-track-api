import io
import pandas as pd
from datetime import datetime
from src.app.core.helpers import datetime_helper
from src.app.core.schema import MessageResponse
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.core.exception.decorator import service_handle_exceptions
from src.app.domain.employee.repository.interface import IPositionRepository
from src.app.domain.employee.service.interface import IPositionService
from src.app.domain.employee.model import Position
from src.app.domain.employee.dto.request import PositionRequestDTO
from src.app.domain.employee.dto.response import PositionPage, PositionResponseDTO


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

    @service_handle_exceptions
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
                message="Position already exists",
                details=f"Position with name '{position_request.name}' already exists.",
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

    @service_handle_exceptions
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

    @service_handle_exceptions
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
                message="Position not found",
                details=f"Position with ID {position_id} not found.",
            )
        position = await self.position_repository.get_by_id(position_id)

        if position.name != position_request.name:
            existing_position = await self.position_repository.exists_by(
                name=position_request.name
            )
            if existing_position:
                raise ConflictException(
                    message="Position name already exists",
                    details=f"Position with name '{position_request.name}' already exists.",
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

    @service_handle_exceptions
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
                message="Position not found",
                details=f"Position with ID {position_id} not found.",
            )
        response = await self.position_repository.delete(position_id)
        if response is True:
            return MessageResponse(
                message="Position deleted successfully.",
                success=True,
                details=f"Position with ID {position_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete position.",
                success=False,
                details=f"Position with ID {position_id} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
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
                message="Position not found",
                details=f"Position with ID {position_id} not found.",
            )
        position = await self.position_repository.get_by_id(position_id)
        return PositionResponseDTO(
            id=position.id,
            name=position.name,
            created_at=position.created_at,
            updated_at=position.updated_at,
        )

    @service_handle_exceptions
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
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid page size",
                details="Page size must be greater than 0.",
            )

        page_result = await self.position_repository.get_pageable(page, size)
        position_response = [
            PositionResponseDTO(**position.__dict__) for position in page_result.data
        ]

        return PositionPage(
            data=position_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
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
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid page size",
                details="Page size must be greater than 0.",
            )

        search_dict = {"name": search_term}

        page_result = await self.position_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                message="No positions found",
                details=f"No positions found matching the search term '{search_term}'.",
            )

        position_response = [
            PositionResponseDTO(**position.__dict__) for position in page_result.data
        ]

        return PositionPage(
            data=position_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
    async def delete_positions_by_ids(self, position_ids: list[int]) -> MessageResponse:
        """
        Delete multiple positions by their IDs.

        :param position_ids: List of position IDs to delete
        :return: Message with the result of the deletion operation
        :raises BadRequestException: If no position IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided position IDs do not exist
        """
        if len(position_ids) == 0:
            raise BadRequestException(
                message="No position IDs provided",
                details="Please provide a list of position IDs to delete.",
            )

        invalid_ids = [id for id in position_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid position IDs",
                details=f"Position IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        positions = await self.position_repository.find_by_ids(position_ids)

        found_ids = {
            position["id"] if isinstance(position, dict) else position.id
            for position in positions
        }

        missing_ids = [id for id in position_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Positions not found",
                details=f"Positions with IDs {missing_ids} not found. Cannot proceed with deletion.",
            )

        resp = await self.position_repository.delete_by_ids(position_ids)

        if resp is True:
            return MessageResponse(
                message="Positions deleted successfully.",
                success=True,
                details=f"Positions with IDs {position_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete positions.",
                success=False,
                details=f"Positions with IDs {position_ids} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
    async def export_positions_to_excel(self, position_ids: list[int]) -> bytes:
        """
        Export positions to Excel format by their IDs.

        :param position_ids: List of position IDs to export
        :return: Excel file as bytes
        :raises BadRequestException: If no position IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided position IDs do not exist
        """
        if len(position_ids) == 0:
            raise BadRequestException(
                message="No position IDs provided",
                details="Please provide a list of position IDs to export.",
            )

        invalid_ids = [id for id in position_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid position IDs",
                details=f"Position IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        positions = await self.position_repository.find_by_ids(position_ids)

        found_ids = {
            position["id"] if isinstance(position, dict) else position.id
            for position in positions
        }
        missing_ids = [id for id in position_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Positions not found",
                details=f"Positions with IDs {missing_ids} not found. Cannot proceed with export.",
            )

        positions_data = [
            {
                "ID": position.id,
                "Name": position.name,
                "Created At": datetime_helper.to_lima_timezone(position.created_at),
                "Updated At": datetime_helper.to_lima_timezone(position.updated_at),
            }
            for position in positions
        ]

        df = pd.DataFrame(positions_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Positions", index=False)

            worksheet = writer.sheets["Positions"]
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)

        output.seek(0)
        return output.getvalue()
