from datetime import datetime
from src.app.model.entity import Ambito
from src.app.dto.request import DocumentaryTopicRequestDTO
from src.app.dto.response import DocumentaryTopicPage, DocumentaryTopicResponseDTO
from src.app.schema import MessageResponse
from src.app.exception import BadRequestException, ConflictException, NotFoundException
from src.app.exception.decorator import handle_exceptions
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.service.interfaces import IDocumentaryTopicService


class DocumentaryTopicServiceImpl(IDocumentaryTopicService):
    """
    Implementation of the Documentary Topic Service interface.
    Handles business logic for documentary topics operations.
    """

    def __init__(self, repository: IDocumentaryTopicRepository):
        """
        Initializes the Documentary Topic Service with a repository.

        Args:
            repository: The repository for documentary topic data access
        """
        self.repository = repository

    @handle_exceptions
    async def add_documentary_topic(
        self,
        documentary_topic_request: DocumentaryTopicRequestDTO
    ) -> DocumentaryTopicResponseDTO:
        """
        Adds a new documentary topic to the system.

        Args:
            documentary_topic_request: DTO containing the documentary topic details

        Returns:
            DTO with the created documentary topic data

        Raises:
            ConflictException: If a documentary topic with the same name already exists
        """
        existing_topic = await self.repository.exists_by(nombre=documentary_topic_request.nombre)
        if existing_topic:
            raise ConflictException(
                details=f"Documentary topic with name {documentary_topic_request.nombre} already exists",
            )

        new_topic = Ambito(
            nombre=documentary_topic_request.nombre,
        )

        created_topic = await self.repository.save(new_topic)

        return DocumentaryTopicResponseDTO(
            id=created_topic.id,
            nombre=created_topic.nombre,
            created_at=created_topic.created_at,
            updated_at=created_topic.updated_at,
        )

    @handle_exceptions
    async def get_all_documentary_topics(self) -> list[DocumentaryTopicResponseDTO]:
        """
        Retrieves all documentary topics from the database.

        Returns:
            List of DTOs containing all documentary topics
        """
        topics = await self.repository.get_all()
        return [
            DocumentaryTopicResponseDTO(
                id=topic.id,
                nombre=topic.nombre,
                created_at=topic.created_at,
                updated_at=topic.updated_at
            )
            for topic in topics
        ]

    @handle_exceptions
    async def update_documentary_topic(
        self,
        documentary_topic_id: int,
        documentary_topic_request: DocumentaryTopicRequestDTO
    ) -> DocumentaryTopicResponseDTO:
        """
        Updates an existing documentary topic.

        Args:
            documentary_topic_id: ID of the documentary topic to update
            documentary_topic_request: DTO containing the updated documentary topic details

        Returns:
            DTO with the updated documentary topic data

        Raises:
            NotFoundException: If the documentary topic with the given ID doesn't exist
            ConflictException: If another documentary topic with the same name already exists
        """
        exists_topic_id = await self.repository.exists_by(id=documentary_topic_id)
        if not exists_topic_id:
            raise NotFoundException(
                details=f"Documentary topic with id {documentary_topic_id} not found",
            )
        topic = await self.repository.get_by_id(documentary_topic_id)

        if topic.nombre != documentary_topic_request.nombre:
            existing_topic = await self.repository.exists_by(nombre=documentary_topic_request.nombre)
            if existing_topic:
                raise ConflictException(
                    details=f"Documentary topic with name {documentary_topic_request.nombre} already exists",
                )

        topic.nombre = documentary_topic_request.nombre
        topic.updated_at = datetime.now()

        updated_topic = await self.repository.save(topic)

        return DocumentaryTopicResponseDTO(
            id=updated_topic.id,
            nombre=updated_topic.nombre,
            created_at=updated_topic.created_at,
            updated_at=updated_topic.updated_at,
        )

    @handle_exceptions
    async def delete_documentary_topic(self, documentary_topic_id: int) -> MessageResponse:
        """
        Deletes a documentary topic by its ID.

        Args:
            documentary_topic_id: ID of the documentary topic to delete

        Returns:
            Message response indicating success or failure

        Raises:
            NotFoundException: If the documentary topic with the given ID doesn't exist
        """
        existing_topic_id = await self.repository.exists_by(id=documentary_topic_id)
        if not existing_topic_id:
            raise NotFoundException(
                details=f"Documentary topic with id {documentary_topic_id} not found",
            )
        response = await self.repository.delete(documentary_topic_id)
        if response is True:
            return MessageResponse(
                message="Documentary topic deleted successfully.",
                success=True,
                details=f"Documentary topic with id {documentary_topic_id} deleted successfully.",
                status_code=200
            )
        else:
            return MessageResponse(
                message="Failed to delete documentary topic.",
                success=False,
                details=f"Documentary topic with id {documentary_topic_id} could not be deleted.",
                status_code=500
            )

    @handle_exceptions
    async def get_documentary_topic_by_id(self, documentary_topic_id: int) -> DocumentaryTopicResponseDTO:
        """
        Retrieves a documentary topic by its ID.

        Args:
            documentary_topic_id: ID of the documentary topic to retrieve

        Returns:
            DTO with the documentary topic data

        Raises:
            NotFoundException: If the documentary topic with the given ID doesn't exist
        """
        existing_topic_id = await self.repository.exists_by(id=documentary_topic_id)
        if not existing_topic_id:
            raise NotFoundException(
                details=f"Documentary topic with id {documentary_topic_id} not found",
            )
        topic = await self.repository.get_by_id(documentary_topic_id)
        return DocumentaryTopicResponseDTO(
            id=topic.id,
            nombre=topic.nombre,
            created_at=topic.created_at,
            updated_at=topic.updated_at
        )

    @handle_exceptions
    async def get_documentary_topics_paginated(self, page: int, size: int) -> DocumentaryTopicPage:
        """
        Retrieves a paginated list of documentary topics.

        Args:
            page: Page number to retrieve
            size: Number of items per page

        Returns:
            Paginated documentary topics with metadata

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
        topic_response = [
            DocumentaryTopicResponseDTO(**topic.__dict__) for topic in page_result.data
        ]

        return DocumentaryTopicPage(
            data=topic_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(self, page: int, size: int, search_term: str) -> DocumentaryTopicPage:
        """
        Searches for documentary topics matching the given search term.

        Args:
            page: Page number to retrieve
            size: Number of items per page
            search_term: Term to search for in documentary topic names

        Returns:
            Paginated documentary topics matching the search criteria

        Raises:
            BadRequestException: If page or size parameters are invalid
            NotFoundException: If no documentary topics match the search criteria
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

        search_dict = {
            "nombre": search_term
        }

        page_result = await self.repository.find(page, size, search_dict)

        if not page_result.data:
            raise NotFoundException(
                details=f"No documentary topics found with the search term {search_term}",
            )

        topic_response = [DocumentaryTopicResponseDTO(**topic.__dict__) for topic in page_result.data]

        return DocumentaryTopicPage(
            data=topic_response,
            meta=page_result.meta,
        )