import io
import pandas as pd
from datetime import datetime
from src.app.core.schema import MessageResponse
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.core.exception.decorator import handle_exceptions
from src.app.core.helpers import datetime_helper
from src.app.domain.location.repository.interface import (
    IHamletRepository,
    ISettlementRepository,
)
from src.app.domain.location.service.interface import IHamletService
from src.app.domain.location.model import Hamlet
from src.app.domain.location.dto.request import HamletRequestDTO
from src.app.domain.location.dto.response import HamletResponseDTO, HamletPage


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
                message="Hamlet already exists",
                details=f"Hamlet with name '{hamlet_request.name}' already exists.",
            )

        if hamlet_request.settlement_id is not None:
            existing_settlement = await self.settlement_repository.exists_by(
                id=hamlet_request.settlement_id
            )
            if not existing_settlement:
                raise NotFoundException(
                    message="Settlement not found",
                    details=f"Settlement with ID {hamlet_request.settlement_id} not found.",
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
                settlement_name=None,
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
                message="Hamlet not found",
                details=f"Hamlet with ID {hamlet_id} not found.",
            )

        hamlet = await self.hamlet_repository.get_by_id(hamlet_id)

        if hamlet.name != hamlet_request.name:
            existing_hamlet = await self.hamlet_repository.exists_by(
                name=hamlet_request.name
            )
            if existing_hamlet:
                raise ConflictException(
                    message="Hamlet name already exists",
                    details=f"Hamlet with name '{hamlet_request.name}' already exists.",
                )

        if hamlet_request.settlement_id is not None:
            existing_settlement = await self.settlement_repository.exists_by(
                id=hamlet_request.settlement_id
            )
            if not existing_settlement:
                raise NotFoundException(
                    message="Settlement not found",
                    details=f"Settlement with ID {hamlet_request.settlement_id} not found.",
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
                message="Hamlet not found",
                details=f"Hamlet with ID {hamlet_id} not found.",
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
                message="Hamlet not found",
                details=f"Hamlet with ID {hamlet_id} not found.",
            )

        hamlet = await self.hamlet_repository.get_by_id(hamlet_id)

        return HamletResponseDTO(
            id=hamlet.id,
            name=hamlet.name,
            settlement_id=hamlet.settlement_id,
            settlement_name=None,
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
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid page size",
                details="Page size must be greater than 0.",
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
                details="Page number must be greater than 0.",
            )
        if size < 1:
            raise BadRequestException(
                message="Invalid page size",
                details="Page size must be greater than 0.",
            )

        search_dict = {"name": search_term}

        page_result = await self.hamlet_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                message="No hamlets found",
                details=f"No hamlets found matching the search term '{search_term}'.",
            )

        hamlet_response = [
            HamletResponseDTO(**hamlet_dict) for hamlet_dict in page_result.data
        ]

        return HamletPage(
            data=hamlet_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def delete_hamlets_by_ids(self, hamlet_ids: list[int]) -> MessageResponse:
        """
        Delete multiple hamlets by their IDs.

        :param hamlet_ids: List of hamlet IDs to delete
        :return: Message with the result of the deletion operation
        :raises BadRequestException: If no hamlet IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided hamlet IDs do not exist
        """
        if len(hamlet_ids) == 0:
            raise BadRequestException(
                message="No hamlet IDs provided",
                details="Please provide a list of hamlet IDs to delete.",
            )

        invalid_ids = [id for id in hamlet_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid hamlet IDs",
                details=f"Hamlet IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        hamlets = await self.hamlet_repository.find_by_ids(hamlet_ids)

        found_ids = {hamlet.id for hamlet in hamlets}

        missing_ids = [id for id in hamlet_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Hamlets not found",
                details=f"Hamlets with IDs {missing_ids} not found. Cannot proceed with deletion.",
            )

        resp = await self.hamlet_repository.delete_by_ids(hamlet_ids)

        if resp is True:
            return MessageResponse(
                message="Hamlets deleted successfully.",
                success=True,
                details=f"Hamlets with IDs {hamlet_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete hamlets.",
                success=False,
                details=f"Hamlets with IDs {hamlet_ids} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def export_hamlets_to_excel(self, hamlet_ids: list[int]) -> bytes:
        """
        Export hamlets to Excel format by their IDs.

        :param hamlet_ids: List of hamlet IDs to export
        :return: Excel file as bytes
        :raises BadRequestException: If no hamlet IDs are provided or if any ID is invalid
        :raises NotFoundException: If any of the provided hamlet IDs do not exist
        """
        if len(hamlet_ids) == 0:
            raise BadRequestException(
                message="No hamlet IDs provided",
                details="Please provide a list of hamlet IDs to export.",
            )

        invalid_ids = [id for id in hamlet_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid hamlet IDs",
                details=f"Hamlet IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        hamlets = await self.hamlet_repository.find_by_ids(hamlet_ids)

        found_ids = {hamlet.id for hamlet in hamlets}
        missing_ids = [id for id in hamlet_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Hamlets not found",
                details=f"Hamlets with IDs {missing_ids} not found. Cannot proceed with export.",
            )

        hamlets_data = [
            {
                "ID": hamlet.id,
                "Name": hamlet.name,
                "Settlement ID": hamlet.settlement_id,
                "Settlement Name": (
                    hamlet.settlement.name if hamlet.settlement else "N/A"
                ),
                "Created At": datetime_helper.to_lima_timezone(hamlet.created_at),
                "Updated At": datetime_helper.to_lima_timezone(hamlet.updated_at),
            }
            for hamlet in hamlets
        ]

        df = pd.DataFrame(hamlets_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Hamlets", index=False)

            worksheet = writer.sheets["Hamlets"]
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)

        output.seek(0)
        return output.getvalue()
