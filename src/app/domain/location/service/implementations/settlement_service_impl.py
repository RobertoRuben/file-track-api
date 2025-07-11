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
from src.app.domain.location.model import Settlement
from src.app.domain.location.repository.interface import ISettlementRepository
from src.app.domain.location.service.interface import ISettlementService
from src.app.domain.location.dto.request import SettlementRequestDTO
from src.app.domain.location.dto.response import SettlementPage, SettlementResponseDTO


class SettlementServiceImpl(ISettlementService):
    """
    Implementation of the Settlement Service interface.
    Handles business logic for settlement operations.

    :ivar settlement_repository: Repository for settlement data access operations
    """

    def __init__(self, settlement_repository: ISettlementRepository):
        """
        Initializes the Settlement Service with a repository.

        :param settlement_repository: The repository for settlement data access
        """
        self.settlement_repository = settlement_repository

    @service_handle_exceptions
    async def add_settlement(
        self, settlement_request: SettlementRequestDTO
    ) -> SettlementResponseDTO:
        """
        Adds a new settlement to the system.

        :param settlement_request: DTO containing the settlement details
        :return: DTO with the created settlement data
        :raises ConflictException: If a settlement with the same name already exists
        """
        existing_settlement = await self.settlement_repository.exists_by(
            name=settlement_request.name
        )
        if existing_settlement:
            raise ConflictException(
                message="Settlement already exists",
                details=f"Settlement with name {settlement_request.name} already exists",
            )

        new_settlement = Settlement(
            name=settlement_request.name,
        )

        created_settlement = await self.settlement_repository.save(new_settlement)

        return SettlementResponseDTO(
            id=created_settlement.id,
            name=created_settlement.name,
            created_at=created_settlement.created_at,
            updated_at=created_settlement.updated_at,
        )

    @service_handle_exceptions
    async def get_all_settlements(self) -> list[SettlementResponseDTO]:
        """
        Retrieves all settlements from the database.

        :return: List of DTOs containing all settlements
        """
        settlements = await self.settlement_repository.get_all()
        return [
            SettlementResponseDTO(
                id=settlement.id,
                name=settlement.name,
                created_at=settlement.created_at,
                updated_at=settlement.updated_at,
            )
            for settlement in settlements
        ]

    @service_handle_exceptions
    async def update_settlement(
        self, settlement_id: int, settlement_request: SettlementRequestDTO
    ) -> SettlementResponseDTO:
        """
        Updates an existing settlement.

        :param settlement_id: ID of the settlement to update
        :param settlement_request: DTO containing the updated settlement details
        :return: DTO with the updated settlement data
        :raises NotFoundException: If the settlement with the given ID doesn't exist
        :raises ConflictException: If another settlement with the same name already exists
        """
        exists_settlement_id = await self.settlement_repository.exists_by(
            id=settlement_id
        )
        if not exists_settlement_id:
            raise NotFoundException(
                message="Settlement not found",
                details=f"Settlement with id {settlement_id} not found",
            )
        settlement = await self.settlement_repository.get_by_id(settlement_id)

        if settlement.name != settlement_request.name:
            existing_settlement = await self.settlement_repository.exists_by(
                name=settlement_request.name
            )
            if existing_settlement:
                raise ConflictException(
                    message="Settlement name already exists",
                    details=f"Settlement with name {settlement_request.name} already exists",
                )

        settlement.name = settlement_request.name
        settlement.updated_at = datetime.now()

        updated_settlement = await self.settlement_repository.save(settlement)

        return SettlementResponseDTO(
            id=updated_settlement.id,
            name=updated_settlement.name,
            created_at=updated_settlement.created_at,
            updated_at=updated_settlement.updated_at,
        )

    @service_handle_exceptions
    async def delete_settlement(self, settlement_id: int) -> MessageResponse:
        """
        Deletes a settlement by its ID.

        :param settlement_id: ID of the settlement to delete
        :return: Message response indicating success or failure
        :raises NotFoundException: If the settlement with the given ID doesn't exist
        """
        existing_settlement_id = await self.settlement_repository.exists_by(
            id=settlement_id
        )
        if not existing_settlement_id:
            raise NotFoundException(
                message="Settlement not found",
                details=f"Settlement with id {settlement_id} not found",
            )
        response = await self.settlement_repository.delete(settlement_id)
        if response is True:
            return MessageResponse(
                message="Settlement deleted successfully.",
                success=True,
                details=f"Settlement with id {settlement_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete settlement.",
                success=False,
                details=f"Settlement with id {settlement_id} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
    async def get_settlement_by_id(self, settlement_id: int) -> SettlementResponseDTO:
        """
        Retrieves a settlement by its ID.

        :param settlement_id: ID of the settlement to retrieve
        :return: DTO with the settlement data
        :raises NotFoundException: If the settlement with the given ID doesn't exist
        """
        existing_settlement_id = await self.settlement_repository.exists_by(
            id=settlement_id
        )
        if not existing_settlement_id:
            raise NotFoundException(
                message="Settlement not found",
                details=f"Settlement with id {settlement_id} not found",
            )
        settlement = await self.settlement_repository.get_by_id(settlement_id)
        return SettlementResponseDTO(
            id=settlement.id,
            name=settlement.name,
            created_at=settlement.created_at,
            updated_at=settlement.updated_at,
        )

    @service_handle_exceptions
    async def get_settlements_paginated(self, page: int, size: int) -> SettlementPage:
        """
        Retrieves a paginated list of settlements.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :return: Paginated settlements with metadata
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

        page_result = await self.settlement_repository.get_pageable(page, size)
        settlement_response = [
            SettlementResponseDTO(
                id=settlement.id,
                name=settlement.name,
                created_at=settlement.created_at,
                updated_at=settlement.updated_at,
            )
            for settlement in page_result.data
        ]

        return SettlementPage(
            data=settlement_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> SettlementPage:
        """
        Searches for settlements matching the given search term.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :param search_term: Term to search for in settlement names
        :return: Paginated settlements matching the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no settlements match the search criteria
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

        page_result = await self.settlement_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                message="No settlements found",
                details=f"No settlements found with the search term {search_term}",
            )

        settlement_response = [
            SettlementResponseDTO(
                id=settlement.id,
                name=settlement.name,
                created_at=settlement.created_at,
                updated_at=settlement.updated_at,
            )
            for settlement in page_result.data
        ]

        return SettlementPage(
            data=settlement_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
    async def delete_settlements_by_ids(
        self, settlement_ids: list[int]
    ) -> MessageResponse:
        """
        Deletes multiple settlements by their IDs.

        :param settlement_ids: List of IDs of the settlements to delete
        :return: Message response indicating success or failure
        :raises NotFoundException: If none of the settlements with the given IDs exist
        :raises BadRequestException: If the settlement_ids list is empty
        """
        if len(settlement_ids) == 0:
            raise BadRequestException(
                message="Invalid settlement IDs",
                details="Settlement IDs list cannot be empty.",
            )

        invalid_ids = [id for id in settlement_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid settlement IDs",
                details=f"Settlement IDs must be positive integers. Invalid IDs: {invalid_ids}",
            )

        settlements = await self.settlement_repository.find_by_ids(settlement_ids)

        found_ids = {
            settlement["id"] if isinstance(settlement, dict) else settlement.id
            for settlement in settlements
        }
        missing_ids = [id for id in settlement_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Settlements not found",
                details=f"Settlements with ids {missing_ids} not found.",
            )

        resp = await self.settlement_repository.delete_by_ids(settlement_ids)

        if resp is True:
            return MessageResponse(
                message="Settlements deleted successfully.",
                success=True,
                details=f"Settlements with ids {settlement_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete settlements.",
                success=False,
                details=f"Settlements with ids {settlement_ids} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
    async def export_settlements_to_excel(self, settlement_ids) -> bytes:
        """
        Exports settlements to an Excel file.

        :param settlement_ids: List of IDs of the settlements to export
        :return: Bytes of the Excel file containing the settlements
        :raises NotFoundException: If none of the settlements with the given IDs exist
        :raises BadRequestException: If the settlement_ids list is empty or contains invalid IDs
        """
        if len(settlement_ids) == 0:
            raise BadRequestException(
                message="Invalid settlement IDs",
                details="Settlement IDs list cannot be empty.",
            )

        invalid_ids = [id for id in settlement_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid settlement IDs",
                details=f"Settlement IDs must be positive integers. Invalid IDs: {invalid_ids}",
            )

        settlements = await self.settlement_repository.find_by_ids(settlement_ids)

        found_ids = {
            settlement["id"] if isinstance(settlement, dict) else settlement.id
            for settlement in settlements
        }
        missing_ids = [id for id in settlement_ids if id not in found_ids]
        if missing_ids:
            raise NotFoundException(
                message="Settlements not found",
                details=f"Settlements with ids {missing_ids} not found.",
            )

        settlements_data = [
            {
                "ID": settlement.id,
                "Nombre": settlement.name,
                "Fecha de Creación": datetime_helper.to_lima_timezone(
                    settlement.created_at
                ),
                "Updated At": datetime_helper.to_lima_timezone(settlement.updated_at),
            }
            for settlement in settlements
        ]

        df = pd.DataFrame(settlements_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Settlements")

            worksheet = writer.sheets["Settlements"]
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_length)

        output.seek(0)
        return output.getvalue()
