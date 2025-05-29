import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import ISubmitterRepository
from src.app.model.entity import Submitter
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination


class SubmitterRepositoryImpl(ISubmitterRepository):
    """
    Repository implementation for handling Submitter entities.
    Provides methods for CRUD operations and search functionality.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, submitter: Submitter) -> Submitter:
        """
        Save a submitter to the database.

        :param submitter: The Submitter entity to save
        :return: The persisted Submitter with updated attributes
        :raises: DatabaseException if an error occurs during the save operation
        """
        self.session.add(submitter)
        return submitter

    @transactional(readonly=True)
    async def get_all(self) -> list[Submitter]:
        """
        Retrieve all submitters from the database.

        :return: A list of all Submitter entities
        :raises: DatabaseException if an error occurs while retrieving submitters
        """
        stmt = select(Submitter)
        results = await self.session.exec(stmt)
        submitters = results.all()
        return list(submitters)

    @transactional(readonly=False)
    async def delete(self, submitter_id: int) -> bool:
        """
        Delete a submitter by its ID.

        :param submitter_id: The ID of the submitter to delete
        :return: True if the deletion was successful
        :raises: DatabaseException if an error occurs during deletion
        """
        submitter = await self.get_by_id(submitter_id)
        await self.session.delete(submitter)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, submitter_id: int) -> Submitter:
        """
        Retrieve a submitter by its ID.

        :param submitter_id: The ID of the submitter to retrieve
        :return: The Submitter entity with the given ID
        :raises: DatabaseException if an error occurs during retrieval
        """
        stmt = select(Submitter).where(Submitter.id == submitter_id)
        results = await self.session.exec(stmt)
        submitter = results.first()
        return submitter

    @transactional(readonly=True)
    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Retrieve submitters with pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :return: A Page object containing the submitters and pagination metadata
        :raises: DatabaseException if an error occurs during the paginated query
        """
        offset_value = (page - 1) * size
        stmt = select(Submitter)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        submitters = list(results.all())

        count_stmt = select(func.count(Submitter.id))
        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1

        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        pagination_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(data=submitters, meta=pagination_info)

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search submitters with filtering and pagination, case-insensitive.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :param search_dict: Dictionary of field-value pairs to search for
        :return: A Page object containing the filtered submitters and pagination metadata
        :raises: DatabaseException if an error occurs during the search operation
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["names", "dni", "paternal_surname", "maternal_surname"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "dni":
                try:
                    dni_value = int(search_value)
                    conditions.append(Submitter.dni == dni_value)
                except ValueError:
                    conditions.append(
                        func.cast(Submitter.dni, func.text("text")).like(
                            f"{search_value}%"
                        )
                    )
            else:
                normalized_search = search_value.lower()

                if field_name == "names":
                    field = Submitter.names
                elif field_name == "paternal_surname":
                    field = Submitter.paternal_surname
                elif field_name == "maternal_surname":
                    field = Submitter.maternal_surname

                conditions.append(func.lower(field) == normalized_search)
                conditions.append(func.lower(field).like(f"{normalized_search}%"))
                conditions.append(
                    func.lower(field).like(f"%{normalized_search}%")
                )  # Contains

        stmt = select(Submitter)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        submitters = list(results.all())

        count_stmt = select(func.count(Submitter.id))

        if conditions:
            count_stmt = count_stmt.where(or_(*conditions))

        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()

        total_pages = math.ceil(total_items / size) if total_items > 0 else 1
        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        pagination_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(data=submitters, meta=pagination_info)

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a submitter exists based on the provided criteria.

        :param kwargs: Field-value pairs to check against
        :return: True if a matching submitter exists, False otherwise
        :raises: InvalidFieldException if an invalid field name is provided
        :raises: DatabaseException if an error occurs during the query
        """
        valid_fields = Submitter.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Submitter model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Submitter.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Submitter, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=False)
    async def delete_by_ids(self, submitter_ids: list[int]) -> bool:
        """
        Delete multiple submitters from the database by their IDs.

        :param submitter_ids: List of submitter IDs to delete
        :return: True if all submitters were successfully deleted, False otherwise

        :raises DatabaseException: If an error occurs during the deletion
        """
        if not submitter_ids:
            return True

        stmt = select(Submitter).where(Submitter.id.in_(submitter_ids))
        results = await self.session.exec(stmt)
        submitters = results.all()

        found_ids = {submitter.id for submitter in submitters}
        if len(found_ids) != len(submitter_ids):
            return False

        for submitter in submitters:
            await self.session.delete(submitter)

        return True

    @transactional(readonly=True)
    async def find_by_ids(self, submitter_ids: list[int]) -> list[Submitter]:
        """
        Retrieve multiple submitters from the database by their IDs.

        :param submitter_ids: List of submitter IDs to retrieve
        :return: List of submitters found

        :raises DatabaseException: If an error occurs during the retrieval
        """
        if not submitter_ids:
            return []

        stmt = select(Submitter).where(Submitter.id.in_(submitter_ids))
        results = await self.session.exec(stmt)
        submitters = results.all()

        return list(submitters)
