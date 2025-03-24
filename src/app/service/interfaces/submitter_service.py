from abc import ABC, abstractmethod
from src.app.dto.request import SubmitterRequestDTO
from src.app.dto.response import SubmitterResponseDTO, SubmitterPage
from src.app.schema import MessageResponse


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

        Args:
            submitter_request: The DTO containing submitter details.

        Returns:
            The created submitter as SubmitterResponseDTO.
        """
        pass

    @abstractmethod
    async def get_all_submitters(self) -> list[SubmitterResponseDTO]:
        """
        Retrieves all submitters.

        Returns:
            A list of SubmitterResponseDTO objects representing all submitters.
        """
        pass

    @abstractmethod
    async def update_submitter(
        self, submitter_id: int, submitter_request: SubmitterRequestDTO
    ) -> SubmitterResponseDTO:
        """
        Updates an existing submitter.

        Args:
            submitter_id: The ID of the submitter to update.
            submitter_request: The DTO containing updated submitter details.

        Returns:
            The updated submitter as SubmitterResponseDTO.
        """
        pass

    @abstractmethod
    async def delete_submitter(self, submitter_id: int) -> MessageResponse:
        """
        Deletes a submitter by its ID.

        Args:
            submitter_id: The ID of the submitter to delete.

        Returns:
            A MessageResponse indicating the result of the deletion.
        """
        pass

    @abstractmethod
    async def get_submitter_by_id(self, submitter_id: int) -> SubmitterResponseDTO:
        """
        Retrieves a submitter by its ID.

        Args:
            submitter_id: The ID of the submitter to retrieve.

        Returns:
            The submitter as SubmitterResponseDTO.
        """
        pass

    @abstractmethod
    async def get_submitters_paginated(self, page: int, size: int) -> SubmitterPage:
        """
        Retrieves a paginated list of submitters.

        Args:
            page: The page number to retrieve.
            size: The number of submitters per page.

        Returns:
            A SubmitterPage object containing the paginated submitters.
        """
        pass

    @abstractmethod
    async def find(self, page: int, size: int, search_term: str) -> SubmitterPage:
        """
        Searches for submitters based on search criteria.

        Args:
            page: The page number to retrieve.
            size: The number of submitters per page.
            search_term: The term to search for in submitter names or other fields.

        Returns:
            A SubmitterPage object containing submitters that match the search criteria.
        """
        pass