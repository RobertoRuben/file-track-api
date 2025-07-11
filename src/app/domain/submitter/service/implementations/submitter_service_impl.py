import io
import pandas as pd
from datetime import datetime
from src.app.core.helpers import datetime_helper
from src.app.core.schema import MessageResponse
from src.app.core.exception.decorator import service_handle_exceptions
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.domain.submitter.repository.interface import ISubmitterRepository
from src.app.domain.submitter.service.interface import ISubmitterService
from src.app.domain.submitter.model import Submitter
from src.app.domain.submitter.dto.request import SubmitterRequestDTO
from src.app.domain.submitter.dto.response import SubmitterResponseDTO, SubmitterPage


class SubmitterServiceImpl(ISubmitterService):
    """
    Implementation of the Submitter Service interface.
    Handles business logic for submitter operations.
    """

    def __init__(self, submitter_repository: ISubmitterRepository):
        """
        Initializes the Submitter Service with a repository.

        :param submitter_repository: The repository for submitter data access
        """
        self.submitter_repository = submitter_repository

    @service_handle_exceptions
    async def add_submitter(
        self, submitter_request: SubmitterRequestDTO
    ) -> SubmitterResponseDTO:
        """
        Adds a new submitter to the system.

        :param submitter_request: DTO containing the submitter details
        :return: DTO with the created submitter data
        :raises ConflictException: If a submitter with the same DNI already exists
        """
        existing_submitter = await self.submitter_repository.exists_by(
            dni=submitter_request.dni
        )
        if existing_submitter:
            raise ConflictException(
                message="Submitter already exists",
                details=f"Submitter with DNI {submitter_request.dni} already exists",
            )

        new_submitter = Submitter(
            dni=submitter_request.dni,
            names=submitter_request.names,
            paternal_surname=submitter_request.paternal_surname,
            maternal_surname=submitter_request.maternal_surname,
            gender=submitter_request.gender.value,
        )

        created_submitter = await self.submitter_repository.save(new_submitter)

        return SubmitterResponseDTO(
            id=created_submitter.id,
            dni=created_submitter.dni,
            names=created_submitter.names,
            paternal_surname=created_submitter.paternal_surname,
            maternal_surname=created_submitter.maternal_surname,
            gender=created_submitter.gender,
            created_at=created_submitter.created_at,
            updated_at=created_submitter.updated_at,
        )

    @service_handle_exceptions
    async def get_all_submitters(self) -> list[SubmitterResponseDTO]:
        """
        Retrieves all submitters from the database.

        :return: List of DTOs containing all submitters
        """
        submitters = await self.submitter_repository.get_all()
        return [
            SubmitterResponseDTO(
                id=submitter.id,
                dni=submitter.dni,
                names=submitter.names,
                paternal_surname=submitter.paternal_surname,
                maternal_surname=submitter.maternal_surname,
                gender=submitter.gender,
                created_at=submitter.created_at,
                updated_at=submitter.updated_at,
            )
            for submitter in submitters
        ]

    @service_handle_exceptions
    async def update_submitter(
        self, submitter_id: int, submitter_request: SubmitterRequestDTO
    ) -> SubmitterResponseDTO:
        """
        Updates an existing submitter.

        :param submitter_id: ID of the submitter to update
        :param submitter_request: DTO containing the updated submitter details
        :return: DTO with the updated submitter data
        :raises NotFoundException: If the submitter with the given ID doesn't exist
        :raises ConflictException: If another submitter with the same DNI already exists
        """
        exists_submitter_id = await self.submitter_repository.exists_by(id=submitter_id)
        if not exists_submitter_id:
            raise NotFoundException(
                message="Submitter not found",
                details=f"Submitter with id {submitter_id} not found",
            )
        submitter = await self.submitter_repository.get_by_id(submitter_id)

        if submitter.dni != submitter_request.dni:
            existing_submitter = await self.submitter_repository.exists_by(
                dni=submitter_request.dni
            )
            if existing_submitter:
                raise ConflictException(
                    message="Submitter DNI already exists",
                    details=f"Submitter with DNI {submitter_request.dni} already exists",
                )

        submitter.dni = submitter_request.dni
        submitter.names = submitter_request.names
        submitter.paternal_surname = submitter_request.paternal_surname
        submitter.maternal_surname = submitter_request.maternal_surname
        submitter.gender = submitter_request.gender.value
        submitter.updated_at = datetime.now()

        updated_submitter = await self.submitter_repository.save(submitter)

        return SubmitterResponseDTO(
            id=updated_submitter.id,
            dni=updated_submitter.dni,
            names=updated_submitter.names,
            paternal_surname=updated_submitter.paternal_surname,
            maternal_surname=updated_submitter.maternal_surname,
            gender=updated_submitter.gender,
            created_at=updated_submitter.created_at,
            updated_at=updated_submitter.updated_at,
        )

    @service_handle_exceptions
    async def delete_submitter(self, submitter_id: int) -> MessageResponse:
        """
        Deletes a submitter by its ID.

        :param submitter_id: ID of the submitter to delete
        :return: Message response indicating success or failure
        :raises NotFoundException: If the submitter with the given ID doesn't exist
        """
        existing_submitter_id = await self.submitter_repository.exists_by(
            id=submitter_id
        )
        if not existing_submitter_id:
            raise NotFoundException(
                message="Submitter not found",
                details=f"Submitter with id {submitter_id} not found",
            )
        response = await self.submitter_repository.delete(submitter_id)
        if response is True:
            return MessageResponse(
                message="Submitter deleted successfully.",
                success=True,
                details=f"Submitter with id {submitter_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete submitter.",
                success=False,
                details=f"Submitter with id {submitter_id} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
    async def get_submitter_by_id(self, submitter_id: int) -> SubmitterResponseDTO:
        """
        Retrieves a submitter by its ID.

        :param submitter_id: ID of the submitter to retrieve
        :return: DTO with the submitter data
        :raises NotFoundException: If the submitter with the given ID doesn't exist
        """
        existing_submitter_id = await self.submitter_repository.exists_by(
            id=submitter_id
        )
        if not existing_submitter_id:
            raise NotFoundException(
                message="Submitter not found",
                details=f"Submitter with id {submitter_id} not found",
            )
        submitter = await self.submitter_repository.get_by_id(submitter_id)
        return SubmitterResponseDTO(
            id=submitter.id,
            dni=submitter.dni,
            names=submitter.names,
            paternal_surname=submitter.paternal_surname,
            maternal_surname=submitter.maternal_surname,
            gender=submitter.gender,
            created_at=submitter.created_at,
            updated_at=submitter.updated_at,
        )

    @service_handle_exceptions
    async def get_submitters_paginated(self, page: int, size: int) -> SubmitterPage:
        """
        Retrieves a paginated list of submitters.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :return: Paginated submitters with metadata
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

        page_result = await self.submitter_repository.get_pageable(page, size)
        submitter_response = [
            SubmitterResponseDTO(
                id=submitter.id,
                dni=submitter.dni,
                names=submitter.names,
                paternal_surname=submitter.paternal_surname,
                maternal_surname=submitter.maternal_surname,
                gender=submitter.gender,
                created_at=submitter.created_at,
                updated_at=submitter.updated_at,
            )
            for submitter in page_result.data
        ]

        return SubmitterPage(
            data=submitter_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> SubmitterPage:
        """
        Searches for submitters matching the given search term.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :param search_term: Term to search for in submitter names or DNI
        :return: Paginated submitters matching the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no submitters match the search criteria
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

        # Search in names, surnames and DNI
        search_dict = {
            "names": search_term,
            "paternal_surname": search_term,
            "maternal_surname": search_term,
            "dni": search_term if search_term and search_term.isdigit() else None,
        }

        page_result = await self.submitter_repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                message="No submitters found",
                details=f"No submitters found with the search term {search_term}",
            )

        submitter_response = [
            SubmitterResponseDTO(
                id=submitter.id,
                dni=submitter.dni,
                names=submitter.names,
                paternal_surname=submitter.paternal_surname,
                maternal_surname=submitter.maternal_surname,
                gender=submitter.gender,
                created_at=submitter.created_at,
                updated_at=submitter.updated_at,
            )
            for submitter in page_result.data
        ]

        return SubmitterPage(
            data=submitter_response,
            meta=page_result.meta,
        )

    @service_handle_exceptions
    async def delete_submitters_by_ids(
        self, submitter_ids: list[int]
    ) -> MessageResponse:
        """
        Delete multiple submitters by their IDs.

        :param submitter_ids: List of submitter IDs to delete
        :return: Message with the result of the deletion operation
        """
        resp = await self.submitter_repository.delete_by_ids(submitter_ids)

        if resp is True:
            return MessageResponse(
                message="Submitters deleted successfully.",
                success=True,
                details=f"Submitters with IDs {submitter_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete submitters.",
                success=False,
                details=f"Submitters with IDs {submitter_ids} could not be deleted.",
                status_code=500,
            )

    @service_handle_exceptions
    async def export_submitters_to_excel(self, submitter_ids: list[int]) -> bytes:
        """
        Export submitters to Excel format by their IDs.

        :param submitter_ids: List of submitter IDs to export
        :return: Excel file as bytes
        :raises NotFoundException: If none of the submitters with the given IDs exist
        """
        submitters = await self.submitter_repository.find_by_ids(submitter_ids)

        if not submitters:
            raise NotFoundException(
                message="Submitters not found",
                details="No submitters found for the provided IDs.",
            )

        submitters_data = [
            {
                "ID": submitter.id,
                "DNI": submitter.dni,
                "Nombres": submitter.names,
                "Apellido Paterno": submitter.paternal_surname,
                "Apellido Materno": submitter.maternal_surname,
                "Género": submitter.gender,
                "Fecha de Creación": datetime_helper.to_lima_timezone(
                    submitter.created_at
                ),
                "Fecha de Actualización": datetime_helper.to_lima_timezone(
                    submitter.updated_at
                ),
            }
            for submitter in submitters
        ]

        df = pd.DataFrame(submitters_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Submitters", index=False)

            worksheet = writer.sheets["Submitters"]
            for i, col in enumerate(df.columns):
                column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, column_width)

        output.seek(0)
        return output.getvalue()
