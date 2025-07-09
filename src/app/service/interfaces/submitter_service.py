from abc import ABC, abstractmethod
from src.app.dto.request import SubmitterRequestDTO
from src.app.dto.response import SubmitterResponseDTO, SubmitterPage
from src.app.core.schema import MessageResponse


class ISubmitterService(ABC):
    """
    Interface for submitter service operations.
    Defines the contract for business logic related to submitters.
    """

    @abstractmethod
    async def add_submitter(
        self, submitter_request: SubmitterRequestDTO
    ) -> SubmitterResponseDTO:
        """
        Adds a new submitter.

        :param submitter_request: The DTO containing submitter details
        :return: The created submitter as SubmitterResponseDTO
        """
        pass

    @abstractmethod
    async def get_all_submitters(self) -> list[SubmitterResponseDTO]:
        """
        Retrieves all submitters.

        :return: A list of SubmitterResponseDTO objects representing all submitters
        """
        pass

    @abstractmethod
    async def update_submitter(
        self, submitter_id: int, submitter_request: SubmitterRequestDTO
    ) -> SubmitterResponseDTO:
        """
        Updates an existing submitter.

        :param submitter_id: The ID of the submitter to update
        :param submitter_request: The DTO containing updated submitter details
        :return: The updated submitter as SubmitterResponseDTO
        """
        pass

    @abstractmethod
    async def delete_submitter(self, submitter_id: int) -> MessageResponse:
        """
        Deletes a submitter by its ID.

        :param submitter_id: The ID of the submitter to delete
        :return: A MessageResponse indicating the result of the deletion
        """
        pass

    @abstractmethod
    async def get_submitter_by_id(self, submitter_id: int) -> SubmitterResponseDTO:
        """
        Retrieves a submitter by its ID.

        :param submitter_id: The ID of the submitter to retrieve
        :return: The submitter as SubmitterResponseDTO
        """
        pass

    @abstractmethod
    async def get_submitters_paginated(self, page: int, size: int) -> SubmitterPage:
        """
        Retrieves a paginated list of submitters.

        :param page: The page number to retrieve
        :param size: The number of submitters per page
        :return: A SubmitterPage object containing the paginated submitters
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> SubmitterPage:
        """
        Searches for submitters based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of submitters per page
        :param search_term: The term to search for in submitter names or other fields
        :return: A SubmitterPage object containing submitters that match the search criteria
        """
        pass

    @abstractmethod
    async def delete_submitters_by_ids(
        self, submitter_ids: list[int]
    ) -> MessageResponse:
        """
        Delete multiple submitters by their IDs.

        :param submitter_ids: List of submitter IDs to delete
        :return: Message with the result of the deletion operation
        """
        pass

    @abstractmethod
    async def export_submitters_to_excel(self, submitter_ids: list[int]) -> bytes:
        """
        Export submitters to Excel format by their IDs.

        :param submitter_ids: List of submitter IDs to export
        :return: Excel file as bytes
        """
        pass
