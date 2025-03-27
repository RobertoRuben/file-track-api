from datetime import datetime
from src.app.model.entity import Caserio
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDto, HamletPage
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IHamletRepository
from src.app.repository.interfaces import ISettlementRepository
from src.app.service.interfaces import IHamletService


class HamletServiceImpl(IHamletService):
    """
    Implementation of the Hamlet Service interface.
    Handles business logic for hamlet operations.
    """

    def __init__(
        self,
        repository: IHamletRepository,
        settlement_repository: ISettlementRepository,
    ):
        """
        Initializes the Hamlet Service with required repositories.

        Args:
            repository: Repository for hamlet data access
            settlement_repository: Repository for settlement/population center data access
        """
        self.repository = repository
        self.settlement_repository = settlement_repository

    @handle_exceptions
    async def add_hamlet(self, hamlet_request: HamletRequestDTO) -> HamletResponseDto:
        """
        Adds a new hamlet to the system.

        Args:
            hamlet_request: DTO containing the hamlet details

        Returns:
            DTO with the created hamlet data

        Raises:
            ConflictException: If a hamlet with the same name already exists
            NotFoundException: If the specified population center does not exist
        """
        existing_hamlet = await self.repository.exists_by(nombre=hamlet_request.nombre)
        if existing_hamlet:
            raise ConflictException(
                details=f"Hamlet with name {hamlet_request.nombre} already exists",
            )

        if hamlet_request.centro_poblado_id is not None:
            existing_settlement = await self.settlement_repository.exists_by(
                id=hamlet_request.centro_poblado_id
            )
            if not existing_settlement:
                raise NotFoundException(
                    details=f"Population center with ID {hamlet_request.centro_poblado_id} does not exist",
                )

        new_hamlet = Caserio(
            nombre=hamlet_request.nombre,
            centro_poblado_id=hamlet_request.centro_poblado_id,
        )

        created_hamlet = await self.repository.save(new_hamlet)

        return HamletResponseDto(
            id=created_hamlet.id,
            nombre=created_hamlet.nombre,
            centro_poblado_id=created_hamlet.centro_poblado_id,
            created_at=created_hamlet.created_at,
            updated_at=created_hamlet.updated_at,
        )

    @handle_exceptions
    async def get_all_hamlets(self) -> list[HamletResponseDto]:
        """
        Retrieves all hamlets from the database.

        Returns:
            List of DTOs containing all hamlets
        """
        hamlets = await self.repository.get_all()
        return [
            HamletResponseDto(
                id=hamlet.id,
                nombre=hamlet.nombre,
                centro_poblado_id=hamlet.centro_poblado_id,
                created_at=hamlet.created_at,
                updated_at=hamlet.updated_at,
            )
            for hamlet in hamlets
        ]

    @handle_exceptions
    async def update_hamlet(
        self, hamlet_id: int, hamlet_request: HamletRequestDTO
    ) -> HamletResponseDto:
        """
        Updates an existing hamlet.

        Args:
            hamlet_id: ID of the hamlet to update
            hamlet_request: DTO containing the updated hamlet details

        Returns:
            DTO with the updated hamlet data

        Raises:
            NotFoundException: If the hamlet with the given ID doesn't exist
            ConflictException: If another hamlet with the same name already exists
            NotFoundException: If the specified population center does not exist
        """
        exists_hamlet_id = await self.repository.exists_by(id=hamlet_id)
        if not exists_hamlet_id:
            raise NotFoundException(
                details=f"Hamlet with ID {hamlet_id} not found",
            )

        hamlet = await self.repository.get_by_id(hamlet_id)

        if hamlet.nombre != hamlet_request.nombre:
            existing_hamlet = await self.repository.exists_by(
                nombre=hamlet_request.nombre
            )
            if existing_hamlet:
                raise ConflictException(
                    details=f"Hamlet with name {hamlet_request.nombre} already exists",
                )

        if hamlet_request.centro_poblado_id is not None:
            existing_settlement = await self.settlement_repository.exists_by(
                id=hamlet_request.centro_poblado_id
            )
            if not existing_settlement:
                raise NotFoundException(
                    details=f"Population center with ID {hamlet_request.centro_poblado_id} does not exist",
                )

        hamlet.nombre = hamlet_request.nombre
        hamlet.centro_poblado_id = hamlet_request.centro_poblado_id
        hamlet.updated_at = datetime.now()

        updated_hamlet = await self.repository.save(hamlet)

        return HamletResponseDto(
            id=updated_hamlet.id,
            nombre=updated_hamlet.nombre,
            centro_poblado_id=updated_hamlet.centro_poblado_id,
            created_at=updated_hamlet.created_at,
            updated_at=updated_hamlet.updated_at,
        )

    @handle_exceptions
    async def delete_hamlet(self, hamlet_id: int) -> MessageResponse:
        """
        Deletes a hamlet by its ID.

        Args:
            hamlet_id: ID of the hamlet to delete

        Returns:
            Message response indicating success or failure

        Raises:
            NotFoundException: If the hamlet with the given ID doesn't exist
        """
        existing_hamlet_id = await self.repository.exists_by(id=hamlet_id)
        if not existing_hamlet_id:
            raise NotFoundException(
                details=f"Hamlet with ID {hamlet_id} not found",
            )

        response = await self.repository.delete(hamlet_id)

        if response is True:
            return MessageResponse(
                message="Hamlet deleted successfully.",
                success=True,
                details=f"Hamlet with ID {hamlet_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete hamlet.",
                success=False,
                details=f"Hamlet with ID {hamlet_id} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def get_hamlet_by_id(self, hamlet_id: int) -> HamletResponseDto:
        """
        Retrieves a hamlet by its ID.

        Args:
            hamlet_id: ID of the hamlet to retrieve

        Returns:
            DTO with the hamlet data

        Raises:
            NotFoundException: If the hamlet with the given ID doesn't exist
        """
        existing_hamlet_id = await self.repository.exists_by(id=hamlet_id)
        if not existing_hamlet_id:
            raise NotFoundException(
                details=f"Hamlet with ID {hamlet_id} not found",
            )

        hamlet = await self.repository.get_by_id(hamlet_id)

        return HamletResponseDto(
            id=hamlet.id,
            nombre=hamlet.nombre,
            centro_poblado_id=hamlet.centro_poblado_id,
            created_at=hamlet.created_at,
            updated_at=hamlet.updated_at,
        )

    @handle_exceptions
    async def get_hamlets_paginated(self, page: int, size: int) -> HamletPage:
        """
        Retrieves a paginated list of hamlets.

        Args:
            page: Page number to retrieve
            size: Number of items per page

        Returns:
            Paginated hamlets with metadata

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
        hamlet_response = [
            HamletResponseDto(**hamlet_dict) for hamlet_dict in page_result.data
        ]

        return HamletPage(
            data=hamlet_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> HamletPage:
        """
        Searches for hamlets based on search criteria.

        Args:
            page: Page number to retrieve
            size: Number of items per page
            search_term: The term to search for in hamlet names

        Returns:
            Paginated hamlets matching the search criteria

        Raises:
            BadRequestException: If page or size parameters are invalid
            NotFoundException: If no hamlets match the search criteria
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
                details=f"No hamlets found with the search term {search_term}",
            )

        hamlet_response = [
            HamletResponseDto(**hamlet_dict) for hamlet_dict in page_result.data
        ]

        return HamletPage(
            data=hamlet_response,
            meta=page_result.meta,
        )
