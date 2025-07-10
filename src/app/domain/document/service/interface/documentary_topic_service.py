from abc import ABC, abstractmethod
from src.app.domain.document.dto.request import DocumentaryTopicRequestDTO
from src.app.domain.document.dto.response import (
    DocumentaryTopicResponseDTO,
    DocumentaryTopicPage,
)
from src.app.core.schema import MessageResponse


class IDocumentaryTopicService(ABC):
    """
    Interface for documentary topic service operations.
    Defines the contract for business logic related to documentary topics.

    This service handles all operations for managing documentary topics, including
    creation, retrieval, update, and deletion.
    """

    @abstractmethod
    async def add_documentary_topic(
        self, documentary_topic_request: DocumentaryTopicRequestDTO
    ) -> DocumentaryTopicResponseDTO:
        """
        Adds a new documentary topic.

        :param documentary_topic_request: The DTO containing documentary topic details
        :return: The created documentary topic as DocumentaryTopicResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_documentary_topics(self) -> list[DocumentaryTopicResponseDTO]:
        """
        Retrieves all documentary topics.

        :return: A list of DocumentaryTopicResponseDTO objects representing all documentary topics
        """
        pass

    @abstractmethod
    async def update_documentary_topic(
        self,
        documentary_topic_id: int,
        documentary_topic_request: DocumentaryTopicRequestDTO,
    ) -> DocumentaryTopicResponseDTO:
        """
        Updates an existing documentary topic.

        :param documentary_topic_id: The ID of the documentary topic to update
        :param documentary_topic_request: The DTO containing updated documentary topic details
        :return: The updated documentary topic as DocumentaryTopicResponseDTO
        """
        pass

    @abstractmethod
    async def delete_documentary_topic(
        self, documentary_topic_id: int
    ) -> MessageResponse:
        """
        Deletes a documentary topic by its ID.

        :param documentary_topic_id: The ID of the documentary topic to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_documentary_topic_by_id(
        self, documentary_topic_id: int
    ) -> DocumentaryTopicResponseDTO:
        """
        Retrieves a documentary topic by its ID.

        :param documentary_topic_id: The ID of the documentary topic to retrieve
        :return: The documentary topic as DocumentaryTopicResponseDTO
        """
        pass

    @abstractmethod
    async def get_documentary_topics_paginated(
        self, page: int, size: int
    ) -> DocumentaryTopicPage:
        """
        Retrieves a paginated list of documentary topics.

        :param page: The page number to retrieve
        :param size: The number of documentary topics per page
        :return: A DocumentaryTopicPage object containing the paginated documentary topics
        """
        pass

    @abstractmethod
    async def find(
        self, page: int, size: int, search_term: str
    ) -> DocumentaryTopicPage:
        """
        Searches for documentary topics based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of documentary topics per page
        :param search_term: The term to search for in documentary topic names
        :return: A DocumentaryTopicPage object containing documentary topics that match the search criteria
        """
        pass

    @abstractmethod
    async def delete_documentary_topic_by_ids(
        self, documentary_topic_ids: list[int]
    ) -> MessageResponse:
        """
        Deletes multiple documentary topics by their IDs.

        :param documentary_topic_ids: A list of IDs of the documentary topics to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def export_documentary_topics_to_excel(
        self, documentary_topic_ids: list[int] = None
    ) -> bytes:
        """
        Exports documentary topics to an Excel file.

        :param documentary_topic_ids: Optional list of IDs to filter the exported topics
        :return: Bytes representing the Excel file containing the documentary topics
        """
        pass
