from datetime import datetime
from src.app.model.entity import CentroPoblado
from src.app.dto.request import SettlementRequestDTO
from src.app.dto.response import SettlementPage, SettlementReponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import ISettlementRepository
from src.app.service.interfaces import ISettlementService


class SettlementServiceImpl(ISettlementService):
    """
    Implementation of the Settlement Service interface.
    Handles business logic for settlement operations.
    """

    def __init__(self, repository: ISettlementRepository):
        """
        Initializes the Settlement Service with a repository.

        Args:
            repository: The repository for settlement data access
        """
        self.repository = repository

    @handle_exceptions
    async def add_settlement(
        self, settlement_request: SettlementRequestDTO
    ) -> SettlementReponseDTO:
        """
        Adds a new settlement to the system.

        Args:
            settlement_request: DTO containing the settlement details

        Returns:
            DTO with the created settlement data

        Raises:
            ConflictException: If a settlement with the same name already exists
        """
        existing_settlement = await self.repository.exists_by(
            nombre=settlement_request.nombre
        )
        if existing_settlement:
            raise ConflictException(
                details=f"Settlement with name {settlement_request.nombre} already exists",
            )

        new_settlement = CentroPoblado(
            nombre=settlement_request.nombre,
        )

        created_settlement = await self.repository.save(new_settlement)

        return SettlementReponseDTO(
            id=created_settlement.id,
            nombre=created_settlement.nombre,
            created_at=created_settlement.created_at,
            updated_at=created_settlement.updated_at,
        )

    @handle_exceptions
    async def get_all_settlements(self) -> list[SettlementReponseDTO]:
        """
        Retrieves all settlements from the database.

        Returns:
            List of DTOs containing all settlements
        """
        settlements = await self.repository.get_all()
        return [
            SettlementReponseDTO(
                id=settlement.id,
                nombre=settlement.nombre,
                created_at=settlement.created_at,
                updated_at=settlement.updated_at,
            )
            for settlement in settlements
        ]

    @handle_exceptions
    async def update_settlement(
        self, settlement_id: int, settlement_request: SettlementRequestDTO
    ) -> SettlementReponseDTO:
        """
        Updates an existing settlement.

        Args:
            settlement_id: ID of the settlement to update
            settlement_request: DTO containing the updated settlement details

        Returns:
            DTO with the updated settlement data

        Raises:
            NotFoundException: If the settlement with the given ID doesn't exist
            ConflictException: If another settlement with the same name already exists
        """
        exists_settlement_id = await self.repository.exists_by(id=settlement_id)
        if not exists_settlement_id:
            raise NotFoundException(
                details=f"Settlement with id {settlement_id} not found",
            )
        settlement = await self.repository.get_by_id(settlement_id)

        if settlement.nombre != settlement_request.nombre:
            existing_settlement = await self.repository.exists_by(
                nombre=settlement_request.nombre
            )
            if existing_settlement:
                raise ConflictException(
                    details=f"Settlement with name {settlement_request.nombre} already exists",
                )

        settlement.nombre = settlement_request.nombre
        settlement.updated_at = datetime.now()

        updated_settlement = await self.repository.save(settlement)

        return SettlementReponseDTO(
            id=updated_settlement.id,
            nombre=updated_settlement.nombre,
            created_at=updated_settlement.created_at,
            updated_at=updated_settlement.updated_at,
        )

    @handle_exceptions
    async def delete_settlement(self, settlement_id: int) -> MessageResponse:
        """
        Deletes a settlement by its ID.

        Args:
            settlement_id: ID of the settlement to delete

        Returns:
            Message response indicating success or failure

        Raises:
            NotFoundException: If the settlement with the given ID doesn't exist
        """
        existing_settlement_id = await self.repository.exists_by(id=settlement_id)
        if not existing_settlement_id:
            raise NotFoundException(
                details=f"Settlement with id {settlement_id} not found",
            )
        response = await self.repository.delete(settlement_id)
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

    @handle_exceptions
    async def get_settlement_by_id(self, settlement_id: int) -> SettlementReponseDTO:
        """
        Retrieves a settlement by its ID.

        Args:
            settlement_id: ID of the settlement to retrieve

        Returns:
            DTO with the settlement data

        Raises:
            NotFoundException: If the settlement with the given ID doesn't exist
        """
        existing_settlement_id = await self.repository.exists_by(id=settlement_id)
        if not existing_settlement_id:
            raise NotFoundException(
                details=f"Settlement with id {settlement_id} not found",
            )
        settlement = await self.repository.get_by_id(settlement_id)
        return SettlementReponseDTO(
            id=settlement.id,
            nombre=settlement.nombre,
            created_at=settlement.created_at,
            updated_at=settlement.updated_at,
        )

    @handle_exceptions
    async def get_settlements_paginated(self, page: int, size: int) -> SettlementPage:
        """
        Retrieves a paginated list of settlements.

        Args:
            page: Page number to retrieve
            size: Number of items per page

        Returns:
            Paginated settlements with metadata

        Raises:
            BadRequestException: If page or size parameters are invalid
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

        page_result = await self.repository.get_pageable(page, size)
        settlement_response = [
            SettlementReponseDTO(
                id=settlement.id,
                nombre=settlement.nombre,
                created_at=settlement.created_at,
                updated_at=settlement.updated_at,
            )
            for settlement in page_result.data
        ]

        return SettlementPage(
            data=settlement_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> SettlementPage:
        """
        Searches for settlements matching the given search term.

        Args:
            page: Page number to retrieve
            size: Number of items per page
            search_term: Term to search for in settlement names

        Returns:
            Paginated settlements matching the search criteria

        Raises:
            BadRequestException: If page or size parameters are invalid
            NotFoundException: If no settlements match the search criteria
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

        search_dict = {"nombre": search_term}

        page_result = await self.repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details=f"No settlements found with the search term {search_term}",
            )

        settlement_response = [
            SettlementReponseDTO(
                id=settlement.id,
                nombre=settlement.nombre,
                created_at=settlement.created_at,
                updated_at=settlement.updated_at,
            )
            for settlement in page_result.data
        ]

        return SettlementPage(
            data=settlement_response,
            meta=page_result.meta,
        )
