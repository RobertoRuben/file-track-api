from datetime import datetime
from src.app.model.entity import Hamlet
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDTO, HamletPage
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
        hamlet_repository: IHamletRepository,
        settlement_repository: ISettlementRepository,
    ):
        """
        Initializes the Hamlet Service with required repositories.

        :param hamlet_repository: Repository for hamlet data access
        :param settlement_repository: Repository for settlement data access
        """
        self.hamlet_repository = hamlet_repository
        self.settlement_repository = settlement_repository

    @handle_exceptions
    async def add_hamlet(self, hamlet_request: HamletRequestDTO) -> HamletResponseDTO:
        """
        Adds a new hamlet to the system.

        :param hamlet_request: DTO containing the hamlet details
        :return: DTO with the created hamlet data
        :raises ConflictException: If a hamlet with the same name already exists
        :raises NotFoundException: If the specified settlement does not exist
        """
        existing_hamlet = await self.hamlet_repository.exists_by(
            name=hamlet_request.name
        )
        if existing_hamlet:
            raise ConflictException(
                details=f"Hamlet with name {hamlet_request.name} already exists",
            )

        if hamlet_request.settlement_id is not None:
            existing_settlement = await self.settlement_repository.exists_by(
                id=hamlet_request.settlement_id
            )
            if not existing_settlement:
                raise NotFoundException(
                    details=f"Settlement with ID {hamlet_request.settlement_id} does not exist",
                )

        new_hamlet = Hamlet(
            name=hamlet_request.name,
            settlement_id=hamlet_request.settlement_id,
        )

        created_hamlet = await self.hamlet_repository.save(new_hamlet)

        return HamletResponseDTO(
            id=created_hamlet.id,
            name=created_hamlet.name,
            settlement_id=created_hamlet.settlement_id,
            settlement_name=None,
            created_at=created_hamlet.created_at,
            updated_at=created_hamlet.updated_at,
        )

    @handle_exceptions
    async def get_all_hamlets(self) -> list[HamletResponseDTO]:
        """
        Retrieves all hamlets from the database.

        :return: List of DTOs containing all hamlets
        """
        hamlets = await self.hamlet_repository.get_all()
        return [
            HamletResponseDTO(
                id=hamlet.id,
                name=hamlet.name,
                settlement_id=hamlet.settlement_id,
                settlement_name=hamlet.settlement.name if hamlet.settlement else None,
                created_at=hamlet.created_at,
                updated_at=hamlet.updated_at,
            )
            for hamlet in hamlets
        ]

    @handle_exceptions
    async def update_hamlet(
        self, hamlet_id: int, hamlet_request: HamletRequestDTO
    ) -> HamletResponseDTO:
        """
        Updates an existing hamlet.

        :param hamlet_id: ID of the hamlet to update
        :param hamlet_request: DTO containing the updated hamlet details
        :return: DTO with the updated hamlet data
        :raises NotFoundException: If the hamlet with the given ID doesn't exist
        :raises ConflictException: If another hamlet with the same name already exists
        :raises NotFoundException: If the specified settlement does not exist
        """
        exists_hamlet_id = await self.hamlet_repository.exists_by(id=hamlet_id)
        if not exists_hamlet_id:
            raise NotFoundException(
                details=f"Hamlet with ID {hamlet_id} not found",
            )

        hamlet = await self.hamlet_repository.get_by_id(hamlet_id)

        if hamlet.name != hamlet_request.name:
            existing_hamlet = await self.hamlet_repository.exists_by(
                name=hamlet_request.name
            )
            if existing_hamlet:
                raise ConflictException(
                    details=f"Hamlet with name {hamlet_request.name} already exists",
                )

        if hamlet_request.settlement_id is not None:
            existing_settlement = await self.settlement_repository.exists_by(
                id=hamlet_request.settlement_id
            )
            if not existing_settlement:
                raise NotFoundException(
                    details=f"Settlement with ID {hamlet_request.settlement_id} does not exist",
                )

        hamlet.name = hamlet_request.name
        hamlet.settlement_id = hamlet_request.settlement_id
        hamlet.updated_at = datetime.now()

        updated_hamlet = await self.hamlet_repository.save(hamlet)

        return HamletResponseDTO(
            id=updated_hamlet.id,
            name=updated_hamlet.name,
            settlement_id=updated_hamlet.settlement_id,
            settlement_name=None,
            created_at=updated_hamlet.created_at,
            updated_at=updated_hamlet.updated_at,
        )

    @handle_exceptions
    async def delete_hamlet(self, hamlet_id: int) -> MessageResponse:
        """
        Deletes a hamlet by its ID.

        :param hamlet_id: ID of the hamlet to delete
        :return: Message response indicating success or failure
        :raises NotFoundException: If the hamlet with the given ID doesn't exist
        """
        existing_hamlet_id = await self.hamlet_repository.exists_by(id=hamlet_id)
        if not existing_hamlet_id:
            raise NotFoundException(
                details=f"Hamlet with ID {hamlet_id} not found",
            )

        response = await self.hamlet_repository.delete(hamlet_id)

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
    async def get_hamlet_by_id(self, hamlet_id: int) -> HamletResponseDTO:
        """
        Retrieves a hamlet by its ID.

        :param hamlet_id: ID of the hamlet to retrieve
        :return: DTO with the hamlet data
        :raises NotFoundException: If the hamlet with the given ID doesn't exist
        """
        existing_hamlet_id = await self.hamlet_repository.exists_by(id=hamlet_id)
        if not existing_hamlet_id:
            raise NotFoundException(
                details=f"Hamlet with ID {hamlet_id} not found",
            )

        hamlet = await self.hamlet_repository.get_by_id(hamlet_id)

        return HamletResponseDTO(
            id=hamlet.id,
            name=hamlet.name,
            settlement_id=hamlet.settlement_id,
            settlement_name=hamlet.settlement.name if hamlet.settlement else None,
            created_at=hamlet.created_at,
            updated_at=hamlet.updated_at,
        )

    @handle_exceptions
    async def get_hamlets_paginated(self, page: int, size: int) -> HamletPage:
        """
        Retrieves a paginated list of hamlets.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :return: Paginated hamlets with metadata
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

        page_result = await self.hamlet_repository.get_pageable(page, size)
        hamlet_response = [
            HamletResponseDTO(**hamlet_dict) for hamlet_dict in page_result.data
        ]

        return HamletPage(
            data=hamlet_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> HamletPage:
        """
        Searches for hamlets based on search criteria.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :param search_term: The term to search for in hamlet names
        :return: Paginated hamlets matching the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no hamlets match the search criteria
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

        page_result = await self.hamlet_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details=f"No hamlets found with the search term {search_term}",
            )

        hamlet_response = [
            HamletResponseDTO(**hamlet_dict) for hamlet_dict in page_result.data
        ]

        return HamletPage(
            data=hamlet_response,
            meta=page_result.meta,
        )
