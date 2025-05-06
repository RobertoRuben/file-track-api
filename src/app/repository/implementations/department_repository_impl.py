import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IDepartmentRepository
from src.app.model.entity import Department
from src.app.exception.invalid_field_exception import InvalidFieldException
from src.app.schema import Page, Pagination


class DepartmentRepositoryImpl(IDepartmentRepository):
    """
    Repository implementation for handling Department entities.
    Provides methods for CRUD operations and search functionality.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, department: Department) -> Department:
        """
        Save a department entity to the database.

        :param department: The Department entity to save
        :return: The persisted Department with updated attributes
        :raises: DatabaseException: If an error occurs during the save operation
        """
        self.session.add(department)
        return department

    @transactional(readonly=True)
    async def get_all(self) -> list[Department]:
        """
        Retrieve all department entities from the database.

        :return: A list of all Department entities
        :raises: DatabaseException: If an error occurs while retrieving departments
        """
        stmt = select(Department)
        results = await self.session.exec(stmt)
        departments = results.all()
        return list(departments)

    @transactional(readonly=False)
    async def delete(self, department_id: int) -> bool:
        """
        Delete a department entity by its ID.

        :param department_id: The ID of the department to delete
        :return: True if the deletion was successful
        :raises: DatabaseException: If an error occurs during deletion
        """
        department = await self.get_by_id(department_id)
        await self.session.delete(department)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, department_id: int) -> Department:
        """
        Retrieve a department entity by its ID.

        :param department_id: The ID of the department to retrieve
        :return: The Department entity with the given ID
        :raises: DatabaseException: If an error occurs during retrieval
        """
        stmt = select(Department).where(Department.id == department_id)
        results = await self.session.exec(stmt)
        department = results.first()
        return department

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve departments with pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :return: A Page object containing the departments and pagination metadata
        :raises: DatabaseException: If an error occurs during the paginated query
        """
        offset = (page - 1) * size
        stmt = select(Department)
        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        departments = list(results.all())

        count_stmt = select(func.count(Department.id))
        count_results = await self.session.exec(count_stmt)
        total_items = count_results.first()
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1

        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        page_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(
            data=departments,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for departments with filtering and pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :param search_dict: Dictionary of field-value pairs to search for
        :return: A Page object containing the filtered departments and pagination metadata
        :raises: DatabaseException: If an error occurs during the search operation
        """
        offset = (page - 1) * size
        conditions = []

        allowed_fields = ["name"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "name":
                normalized_search = search_value.lower()
                conditions.append(
                    func.lower(Department.name).like(f"%{normalized_search}%")
                )

        stmt = select(Department)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        departments = list(results.all())

        count_stmt = select(func.count(Department.id))

        if conditions:
            count_stmt = count_stmt.where(or_(*conditions))

        count_results = await self.session.exec(count_stmt)
        total_items = count_results.first()

        total_pages = math.ceil(total_items / size) if total_items > 0 else 1
        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        page_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(
            data=departments,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a department exists based on the provided criteria.

        :param kwargs: Field-value pairs to check against
        :return: True if a matching department exists, False otherwise
        :raises: InvalidFieldException: If an invalid field name is provided
        :raises: DatabaseException: If an error occurs during the query
        """
        valid_fields = Department.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Department model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Department.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Department, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=False)
    async def delete_by_ids(self, department_ids: list[int]) -> bool:
        """
        Delete multiple department entities from the database by their IDs.

        :param department_ids: List of role IDs to delete
        :return: True if all roles were successfully deleted, False otherwise
        :raises: DatabaseException if an error occurs during deletion
        """
        if not department_ids:
            return True

        stmt = select(Department).where(Department.id.in_(department_ids))
        results = await self.session.exec(stmt)
        departments = results.all()

        found_ids = {department.id for department in departments}
        if len(found_ids) != len(department_ids):
            return False
        for department in departments:
            await self.session.delete(department)

        return True

    @transactional(readonly=True)
    async def find_by_ids(self, department_ids: list[int]) -> list[Department]:
        """
        Find roles by a list of IDs.

        :param department_ids: List of role IDs to retrieve
        :return: List of departments matching the provided IDs
        :raises: DatabaseException if an error occurs during retrieval
        """
        if not department_ids:
            return []

        stmt = select(Department).where(Department.id.in_(department_ids))
        results = await self.session.exec(stmt)
        departments = list(results.all())
        return departments
