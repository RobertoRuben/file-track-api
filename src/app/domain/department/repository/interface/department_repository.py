from abc import ABC, abstractmethod
from src.app.domain.department.model import Department
from src.app.core.schema import Page


class IDepartmentRepository(ABC):
    """
    Interface for the Department repository.
    """

    @abstractmethod
    async def save(self, department: Department) -> Department:
        """
        Save a department.

        :param department: The department to save
        :return: The saved department with updated data
        """
        pass

    @abstractmethod
    async def get_all(self) -> list[Department]:
        """
        Get all departments.

        :return: A list containing all departments
        """
        pass

    @abstractmethod
    async def delete(self, department_id: int) -> bool:
        """
        Delete a department by its ID.

        :param department_id: The ID of the department to delete
        :return: True if the department was successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def get_by_id(self, department_id: int) -> Department:
        """
        Get a department by its ID.

        :param department_id: The ID of the department to retrieve
        :return: The found department
        """
        pass

    @abstractmethod
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Get a paginated list of departments.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing departments and pagination information
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
        Find departments by search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with departments matching the search criteria
        """
        pass

    @abstractmethod
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a department exists based on the given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching department exists, False otherwise
        """
        pass

    @abstractmethod
    async def delete_by_ids(self, department_ids: list[int]) -> bool:
        """
        Delete multiple role entities from the database by their IDs.

        :param department_ids: List of department IDs to delete
        :return: True if the departments were successfully deleted, False otherwise
        """
        pass

    @abstractmethod
    async def find_by_ids(self, department_ids: list[int]) -> list[Department]:
        """
        Retrieve multiple role entities from the database by their IDs.

        :param department_ids: List of department IDs to retrieve
        :return: List of found department entities
        """
        pass
