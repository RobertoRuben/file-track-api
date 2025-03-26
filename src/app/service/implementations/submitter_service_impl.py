from datetime import datetime
from src.app.model.entity import Remitente
from src.app.dto.request import SubmitterRequestDTO
from src.app.dto.response import SubmitterResponseDTO, SubmitterPage
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import ISubmitterRepository
from src.app.service.interfaces import ISubmitterService


class SubmitterServiceImpl(ISubmitterService):
    """
    Implementation of the Submitter Service interface.
    Handles business logic for submitter operations.
    """

    def __init__(self, repository: ISubmitterRepository):
        """
        Initializes the Submitter Service with a repository.

        Args:
            repository: The repository for submitter data access
        """
        self.repository = repository

    @handle_exceptions
    async def add_submitter(
        self, submitter_request: SubmitterRequestDTO
    ) -> SubmitterResponseDTO:
        """
        Adds a new submitter to the system.

        Args:
            submitter_request: DTO containing the submitter details

        Returns:
            DTO with the created submitter data

        Raises:
            ConflictException: If a submitter with the same DNI already exists
        """
        existing_submitter = await self.repository.exists_by(dni=submitter_request.dni)
        if existing_submitter:
            raise ConflictException(
                details=f"Submitter with DNI {submitter_request.dni} already exists",
            )

        new_submitter = Remitente(
            dni=submitter_request.dni,
            nombres=submitter_request.nombres,
            apellido_paterno=submitter_request.apellido_paterno,
            apellido_materno=submitter_request.apellido_materno,
            genero=submitter_request.genero.value,
        )

        created_submitter = await self.repository.save(new_submitter)

        return SubmitterResponseDTO(
            id=created_submitter.id,
            dni=created_submitter.dni,
            nombres=created_submitter.nombres,
            apellido_paterno=created_submitter.apellido_paterno,
            apellido_materno=created_submitter.apellido_materno,
            genero=created_submitter.genero,
            created_at=created_submitter.created_at,
            updated_at=created_submitter.updated_at,
        )

    @handle_exceptions
    async def get_all_submitters(self) -> list[SubmitterResponseDTO]:
        """
        Retrieves all submitters from the database.

        Returns:
            List of DTOs containing all submitters
        """
        submitters = await self.repository.get_all()
        return [
            SubmitterResponseDTO(
                id=submitter.id,
                dni=submitter.dni,
                nombres=submitter.nombres,
                apellido_paterno=submitter.apellido_paterno,
                apellido_materno=submitter.apellido_materno,
                genero=submitter.genero,
                created_at=submitter.created_at,
                updated_at=submitter.updated_at,
            )
            for submitter in submitters
        ]

    @handle_exceptions
    async def update_submitter(
        self, submitter_id: int, submitter_request: SubmitterRequestDTO
    ) -> SubmitterResponseDTO:
        """
        Updates an existing submitter.

        Args:
            submitter_id: ID of the submitter to update
            submitter_request: DTO containing the updated submitter details

        Returns:
            DTO with the updated submitter data

        Raises:
            NotFoundException: If the submitter with the given ID doesn't exist
            ConflictException: If another submitter with the same DNI already exists
        """
        exists_submitter_id = await self.repository.exists_by(id=submitter_id)
        if not exists_submitter_id:
            raise NotFoundException(
                details=f"Submitter with id {submitter_id} not found",
            )
        submitter = await self.repository.get_by_id(submitter_id)

        if submitter.dni != submitter_request.dni:
            existing_submitter = await self.repository.exists_by(
                dni=submitter_request.dni
            )
            if existing_submitter:
                raise ConflictException(
                    details=f"Submitter with DNI {submitter_request.dni} already exists",
                )

        submitter.dni = submitter_request.dni
        submitter.nombres = submitter_request.nombres
        submitter.apellido_paterno = submitter_request.apellido_paterno
        submitter.apellido_materno = submitter_request.apellido_materno
        submitter.genero = submitter_request.genero.value
        submitter.updated_at = datetime.now()

        updated_submitter = await self.repository.save(submitter)

        return SubmitterResponseDTO(
            id=updated_submitter.id,
            dni=updated_submitter.dni,
            nombres=updated_submitter.nombres,
            apellido_paterno=updated_submitter.apellido_paterno,
            apellido_materno=updated_submitter.apellido_materno,
            genero=updated_submitter.genero,
            created_at=updated_submitter.created_at,
            updated_at=updated_submitter.updated_at,
        )

    @handle_exceptions
    async def delete_submitter(self, submitter_id: int) -> MessageResponse:
        """
        Deletes a submitter by its ID.

        Args:
            submitter_id: ID of the submitter to delete

        Returns:
            Message response indicating success or failure

        Raises:
            NotFoundException: If the submitter with the given ID doesn't exist
        """
        existing_submitter_id = await self.repository.exists_by(id=submitter_id)
        if not existing_submitter_id:
            raise NotFoundException(
                details=f"Submitter with id {submitter_id} not found",
            )
        response = await self.repository.delete(submitter_id)
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

    @handle_exceptions
    async def get_submitter_by_id(self, submitter_id: int) -> SubmitterResponseDTO:
        """
        Retrieves a submitter by its ID.

        Args:
            submitter_id: ID of the submitter to retrieve

        Returns:
            DTO with the submitter data

        Raises:
            NotFoundException: If the submitter with the given ID doesn't exist
        """
        existing_submitter_id = await self.repository.exists_by(id=submitter_id)
        if not existing_submitter_id:
            raise NotFoundException(
                details=f"Submitter with id {submitter_id} not found",
            )
        submitter = await self.repository.get_by_id(submitter_id)
        return SubmitterResponseDTO(
            id=submitter.id,
            dni=submitter.dni,
            nombres=submitter.nombres,
            apellido_paterno=submitter.apellido_paterno,
            apellido_materno=submitter.apellido_materno,
            genero=submitter.genero,
            created_at=submitter.created_at,
            updated_at=submitter.updated_at,
        )

    @handle_exceptions
    async def get_submitters_paginated(self, page: int, size: int) -> SubmitterPage:
        """
        Retrieves a paginated list of submitters.

        Args:
            page: Page number to retrieve
            size: Number of items per page

        Returns:
            Paginated submitters with metadata

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
        submitter_response = [
            SubmitterResponseDTO(
                id=submitter.id,
                dni=submitter.dni,
                nombres=submitter.nombres,
                apellido_paterno=submitter.apellido_paterno,
                apellido_materno=submitter.apellido_materno,
                genero=submitter.genero,
                created_at=submitter.created_at,
                updated_at=submitter.updated_at,
            )
            for submitter in page_result.data
        ]

        return SubmitterPage(
            data=submitter_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> SubmitterPage:
        """
        Searches for submitters matching the given search term.

        Args:
            page: Page number to retrieve
            size: Number of items per page
            search_term: Term to search for in submitter names or DNI

        Returns:
            Paginated submitters matching the search criteria

        Raises:
            BadRequestException: If page or size parameters are invalid
            NotFoundException: If no submitters match the search criteria
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

        # Se busca en nombres, apellidos y DNI
        search_dict = {
            "nombres": search_term,
            "apellido_paterno": search_term,
            "apellido_materno": search_term,
            "dni": search_term if search_term and search_term.isdigit() else None,
        }

        page_result = await self.repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details=f"No submitters found with the search term {search_term}",
            )

        submitter_response = [
            SubmitterResponseDTO(
                id=submitter.id,
                dni=submitter.dni,
                nombres=submitter.nombres,
                apellido_paterno=submitter.apellido_paterno,
                apellido_materno=submitter.apellido_materno,
                genero=submitter.genero,
                created_at=submitter.created_at,
                updated_at=submitter.updated_at,
            )
            for submitter in page_result.data
        ]

        return SubmitterPage(
            data=submitter_response,
            meta=page_result.meta,
        )
