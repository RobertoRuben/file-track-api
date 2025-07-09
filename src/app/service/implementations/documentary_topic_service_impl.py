import io
import pandas as pd
from datetime import datetime
from src.app.model.entity import DocumentaryTopic
from src.app.core.helpers import datetime_helper
from src.app.dto.request import DocumentaryTopicRequestDTO
from src.app.dto.response import DocumentaryTopicPage, DocumentaryTopicResponseDTO
from src.app.core.schema import MessageResponse
from src.app.core.exception import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from src.app.core.exception import handle_exceptions
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.service.interfaces import IDocumentaryTopicService


class DocumentaryTopicServiceImpl(IDocumentaryTopicService):
    """
    Implementation of the Documentary Topic Service interface.
    Handles business logic for documentary topics operations.
    """

    def __init__(self, documentary_topic_repository: IDocumentaryTopicRepository):
        """
        Initializes the Documentary Topic Service with a repository.

        :param documentary_topic_repository: The repository for documentary topic data access
        """
        self.documentary_topic_repository = documentary_topic_repository

    @handle_exceptions
    async def add_documentary_topic(
        self, documentary_topic_request: DocumentaryTopicRequestDTO
    ) -> DocumentaryTopicResponseDTO:
        """
        Adds a new documentary topic to the system.

        :param documentary_topic_request: DTO containing the documentary topic details
        :return: DTO with the created documentary topic data
        :raises ConflictException: If a documentary topic with the same name already exists
        """
        existing_topic = await self.documentary_topic_repository.exists_by(
            name=documentary_topic_request.name
        )
        if existing_topic:
            raise ConflictException(
                message="Documentary topic already exists",
                details=f"Documentary topic with name '{documentary_topic_request.name}' already exists.",
            )

        new_topic = DocumentaryTopic(
            name=documentary_topic_request.name,
        )

        created_topic = await self.documentary_topic_repository.save(new_topic)

        return DocumentaryTopicResponseDTO(
            id=created_topic.id,
            name=created_topic.name,
            created_at=created_topic.created_at,
            updated_at=created_topic.updated_at,
        )

    @handle_exceptions
    async def get_all_documentary_topics(self) -> list[DocumentaryTopicResponseDTO]:
        """
        Retrieves all documentary topics from the database.

        :return: List of DTOs containing all documentary topics
        """
        topics = await self.documentary_topic_repository.get_all()
        return [
            DocumentaryTopicResponseDTO(
                id=topic.id,
                name=topic.name,
                created_at=topic.created_at,
                updated_at=topic.updated_at,
            )
            for topic in topics
        ]

    @handle_exceptions
    async def update_documentary_topic(
        self,
        documentary_topic_id: int,
        documentary_topic_request: DocumentaryTopicRequestDTO,
    ) -> DocumentaryTopicResponseDTO:
        """
        Updates an existing documentary topic.

        :param documentary_topic_id: ID of the documentary topic to update
        :param documentary_topic_request: DTO containing the updated documentary topic details
        :return: DTO with the updated documentary topic data
        :raises NotFoundException: If the documentary topic with the given ID doesn't exist
        :raises ConflictException: If another documentary topic with the same name already exists
        """
        exists_topic_id = await self.documentary_topic_repository.exists_by(
            id=documentary_topic_id
        )
        if not exists_topic_id:
            raise NotFoundException(
                message="Documentary topic not found",
                details=f"Documentary topic with ID {documentary_topic_id} not found.",
            )

        topic = await self.documentary_topic_repository.get_by_id(documentary_topic_id)

        if topic.name != documentary_topic_request.name:
            existing_topic = await self.documentary_topic_repository.exists_by(
                name=documentary_topic_request.name
            )
            if existing_topic:
                raise ConflictException(
                    message="Documentary topic name already exists",
                    details=f"Documentary topic with name '{documentary_topic_request.name}' already exists.",
                )

        topic.name = documentary_topic_request.name
        topic.updated_at = datetime.now()

        updated_topic = await self.documentary_topic_repository.save(topic)

        return DocumentaryTopicResponseDTO(
            id=updated_topic.id,
            name=updated_topic.name,
            created_at=updated_topic.created_at,
            updated_at=updated_topic.updated_at,
        )

    @handle_exceptions
    async def delete_documentary_topic(
        self, documentary_topic_id: int
    ) -> MessageResponse:
        """
        Deletes a documentary topic by its ID.

        :param documentary_topic_id: ID of the documentary topic to delete
        :return: Message response indicating success or failure
        :raises NotFoundException: If the documentary topic with the given ID doesn't exist
        """
        existing_topic_id = await self.documentary_topic_repository.exists_by(
            id=documentary_topic_id
        )
        if not existing_topic_id:
            raise NotFoundException(
                message="Documentary topic not found",
                details=f"Documentary topic with ID {documentary_topic_id} not found.",
            )

        response = await self.documentary_topic_repository.delete(documentary_topic_id)
        if response is True:
            return MessageResponse(
                message="Documentary topic deleted successfully.",
                success=True,
                details=f"Documentary topic with ID {documentary_topic_id} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete documentary topic.",
                success=False,
                details=f"Documentary topic with ID {documentary_topic_id} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def get_documentary_topic_by_id(
        self, documentary_topic_id: int
    ) -> DocumentaryTopicResponseDTO:
        """
        Retrieves a documentary topic by its ID.

        :param documentary_topic_id: ID of the documentary topic to retrieve
        :return: DTO with the documentary topic data
        :raises NotFoundException: If the documentary topic with the given ID doesn't exist
        """
        existing_topic_id = await self.documentary_topic_repository.exists_by(
            id=documentary_topic_id
        )
        if not existing_topic_id:
            raise NotFoundException(
                message="Documentary topic not found",
                details=f"Documentary topic with ID {documentary_topic_id} not found.",
            )

        topic = await self.documentary_topic_repository.get_by_id(documentary_topic_id)
        return DocumentaryTopicResponseDTO(
            id=topic.id,
            name=topic.name,
            created_at=topic.created_at,
            updated_at=topic.updated_at,
        )

    @handle_exceptions
    async def get_documentary_topics_paginated(
        self, page: int, size: int
    ) -> DocumentaryTopicPage:
        """
        Retrieves a paginated list of documentary topics.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :return: Paginated documentary topics with metadata
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

        page_result = await self.documentary_topic_repository.get_pageable(page, size)
        topic_response = [
            DocumentaryTopicResponseDTO(
                id=topic.id,
                name=topic.name,
                created_at=topic.created_at,
                updated_at=topic.updated_at,
            )
            for topic in page_result.data
        ]

        return DocumentaryTopicPage(
            data=topic_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def find(
        self, page: int, size: int, search_term: str
    ) -> DocumentaryTopicPage:
        """
        Searches for documentary topics matching the given search term.

        :param page: Page number to retrieve
        :param size: Number of items per page
        :param search_term: Term to search for in documentary topic names
        :return: Paginated documentary topics matching the search criteria
        :raises BadRequestException: If page or size parameters are invalid
        :raises NotFoundException: If no documentary topics match the search criteria
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

        page_result = await self.documentary_topic_repository.find(
            page, size, search_dict
        )

        if not page_result.data:
            raise NotFoundException(
                message="No documentary topics found",
                details=f"No documentary topics found matching the search term '{search_term}'.",
            )

        topic_response = [
            DocumentaryTopicResponseDTO(
                id=topic.id,
                name=topic.name,
                created_at=topic.created_at,
                updated_at=topic.updated_at,
            )
            for topic in page_result.data
        ]

        return DocumentaryTopicPage(
            data=topic_response,
            meta=page_result.meta,
        )

    @handle_exceptions
    async def delete_documentary_topic_by_ids(
        self, documentary_topic_ids: list[int]
    ) -> MessageResponse:
        """
        Deletes multiple documentary topics by their IDs.

        :param documentary_topic_ids: List of documentary topic IDs to delete
        :return: Message response indicating success or failure
        :raises NotFoundException: If none of the documentary topics with the given IDs exist
        :raises BadRequestException: If the documentary_topic_ids list is empty or contains invalid IDs
        """
        if len(documentary_topic_ids) == 0:
            raise BadRequestException(
                message="No documentary topic IDs provided",
                details="Please provide a list of documentary topic IDs to delete.",
            )

        invalid_ids = [id for id in documentary_topic_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid documentary topic IDs",
                details=f"Documentary topic IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        documentary_topics = await self.documentary_topic_repository.find_by_ids(
            documentary_topic_ids
        )

        found_ids = {
            topic["id"] if isinstance(topic, dict) else topic.id
            for topic in documentary_topics
        }
        missing_ids = [id for id in documentary_topic_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Documentary topics not found",
                details=f"Documentary topics with IDs {missing_ids} not found. Cannot proceed with deletion.",
            )

        resp = await self.documentary_topic_repository.delete_by_ids(
            documentary_topic_ids
        )

        if resp is True:
            return MessageResponse(
                message="Documentary topics deleted successfully.",
                success=True,
                details=f"Documentary topics with IDs {documentary_topic_ids} deleted successfully.",
                status_code=200,
            )
        else:
            return MessageResponse(
                message="Failed to delete documentary topics.",
                success=False,
                details=f"Documentary topics with IDs {documentary_topic_ids} could not be deleted.",
                status_code=500,
            )

    @handle_exceptions
    async def export_documentary_topics_to_excel(
        self, documentary_topic_ids: list[int]
    ) -> bytes:
        """
        Exports documentary topics to an Excel file.

        :param documentary_topic_ids: List of documentary topic IDs to export
        :return: Bytes of the generated Excel file
        :raises NotFoundException: If none of the documentary topics with the given IDs exist
        :raises BadRequestException: If the documentary_topic_ids list is empty or contains invalid IDs
        """
        if len(documentary_topic_ids) == 0:
            raise BadRequestException(
                message="No documentary topic IDs provided",
                details="Please provide a list of documentary topic IDs to export.",
            )

        invalid_ids = [id for id in documentary_topic_ids if id <= 0]
        if invalid_ids:
            raise BadRequestException(
                message="Invalid documentary topic IDs",
                details=f"Documentary topic IDs must be greater than 0. Invalid IDs: {invalid_ids}.",
            )

        documentary_topics = await self.documentary_topic_repository.find_by_ids(
            documentary_topic_ids
        )

        found_ids = {
            topic["id"] if isinstance(topic, dict) else topic.id
            for topic in documentary_topics
        }
        missing_ids = [id for id in documentary_topic_ids if id not in found_ids]

        if missing_ids:
            raise NotFoundException(
                message="Documentary topics not found",
                details=f"Documentary topics with IDs {missing_ids} not found. Cannot proceed with export.",
            )

        topics_data = [
            {
                "ID": topic.id,
                "Nombre": topic.name,
                "Fecha de Creación": datetime_helper.to_lima_timezone(topic.created_at),
                "Fecha de Actualización": datetime_helper.to_lima_timezone(
                    topic.updated_at
                ),
            }
            for topic in documentary_topics
        ]

        df = pd.DataFrame(topics_data)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Documentary Topics")

            worksheet = writer.sheets["Documentary Topics"]
            for i, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_length)

        output.seek(0)
        return output.getvalue()
