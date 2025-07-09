from abc import ABC, abstractmethod
from src.app.model.entity import DocumentaryTopic
from src.app.schema import Page


class IDocumentaryTopicRepository(ABC):
    """
    Interface for the Documentary Topic repository.
    """

    @abstractmethod
    async def save(self, documentary_topic: DocumentaryTopic) -> DocumentaryTopic:
        """
        Save a documentary topic.

        :param documentary_topic: The documentary topic to save
        :return: The saved documentary topic with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[DocumentaryTopic]:
        """
        Get all documentary topics.

        :return: A list containing all documentary topics
        """
        pass

    @abstractmethod
    async def delete(self, documentary_topic_id: int) -> bool:
        """
        Delete a documentary topic by its ID.

        :param documentary_topic_id: The ID of the documentary topic to delete
        :return: True if the topic was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, documentary_topic_id: int) -> DocumentaryTopic:
        """
        Get a documentary topic by its ID.

        :param documentary_topic_id: The ID of the documentary topic to retrieve
        :return: The found documentary topic
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Get a paginated list of documentary topics.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing documentary topics and pagination information
        """
        pass

    @abstractmethod
    async def find(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Find documentary topics by search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with documentary topics matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a documentary topic exists based on the given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching documentary topic exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def delete_by_ids(self, documentary_topic_ids: list[int]) -> bool:
        """
        Delete documentary topics by their IDs.

        :param documentary_topic_ids: List of IDs of the documentary topics to delete
        :return: True if the topics were successfully deleted, False otherwise
        """
        pass
    
    @abstractmethod
    async def find_by_ids(self, documentary_topic_ids: list[int]) -> list[DocumentaryTopic]:
        """
        Find documentary topics by their IDs.

        :param documentary_topic_ids: List of IDs of the documentary topics to find
        :return: A list of documentary topics matching the provided IDs
        """
        pass
