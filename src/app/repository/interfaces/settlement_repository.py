from abc import ABC, abstractmethod
from src.app.model.entity import Settlement
from src.app.schema import Page


class ISettlementRepository(ABC):

    @abstractmethod
    async def save(self, settlement: Settlement) -> Settlement:
        """
        Saves a settlement entity to the database.

        :param settlement: The settlement entity to save
        :return: The saved settlement with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Settlement]:
        """
        Retrieves all settlement entities from the database.

        :return: A list containing all settlements
        """
        pass

    @abstractmethod
    async def delete(self, settlement_id: int) -> bool:
        """
        Deletes a settlement entity from the database by its ID.

        :param settlement_id: The ID of the settlement to delete
        :return: True if the settlement was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, settlement_id: int) -> Settlement:
        """
        Retrieves a settlement entity from the database by its ID.

        :param settlement_id: The ID of the settlement to retrieve
        :return: The found settlement entity
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieves a paginated list of settlement entities from the database.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing settlements and pagination information
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
        Retrieves a paginated list of settlement entities based on search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with settlements matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if a settlement entity exists in the database according to specific criteria.

        :param kwargs: Key-value pairs representing search criteria
        :return: True if a matching settlement exists, False otherwise
        """
        pass
