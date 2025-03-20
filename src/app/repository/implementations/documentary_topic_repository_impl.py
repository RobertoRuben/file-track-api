import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.model.entity import Ambito
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination


class DocumentaryTopicRepositoryImpl(IDocumentaryTopicRepository):

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, ambito: Ambito) -> Ambito:
        """
        Save a documentary topic entity to the database.

        Args:
            ambito: The Ambito entity to save

        Returns:
            The persisted Ambito with updated attributes

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        self.session.add(ambito)
        return ambito

    @transactional(readonly=True)
    async def get_all(self) -> list[Ambito]:
        """
        Retrieve all ambito entities from the database.

        Returns:
            A list of all Ambito entities

        Raises:
            DatabaseException: If an error occurs while retrieving roles
        """
        stmt = select(Ambito)
        results = await self.session.exec(stmt)
        documentary_topics = results.all()
        return list(documentary_topics)

    @transactional(readonly=False)
    async def delete(self, ambito_id: int) -> bool:
        """
        Delete a ambito entity by its ID.

        Args:
            ambito_id: The ID of the role to delete

        Returns:
            True if the deletion was successful

        Raises:
            DatabaseException: If an error occurs during deletion
        """
        documentary_topic = await self.get_by_id(ambito_id)
        await self.session.delete(documentary_topic)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, ambito_id: int) -> Ambito:
        """
        Retrieve a ambito entity by its ID.

        Args:
            ambito_id: The ID of the role to retrieve

        Returns:
            The Rol entity with the given ID

        Raises:
            DatabaseException: If an error occurs during retrieval
        """
        stmt = select(Ambito).where(Ambito.id == ambito_id)
        results = await self.session.exec(stmt)
        documentary_topic = results.first()
        return documentary_topic

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve ambitos with pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page

        Returns:
            A Page object containing the roles and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the paginated query
        """
        offset_value = (page - 1) * size
        stmt = select(Ambito)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        documentary_topics = list(results.all())

        count_stmt = select(func.count(Ambito.id))
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
            previous_page=previous_page
        )

        return Page(
            data=documentary_topics,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for ambitos with filtering and pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page
            search_dict: Dictionary of field-value pairs to search for

        Returns:
            A Page object containing the filtered roles and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the search operation
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["nombre"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "nombre":
                normalized_search = search_value.lower()
                conditions.append(func.lower(Ambito.nombre).like(f"%{normalized_search}%"))

        stmt = select(Ambito)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        documentary_topics = list(results.all())

        count_stmt = select(func.count(Ambito.id))

        if conditions:
            count_stmt = count_stmt.where(or_(*conditions))

        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()

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
            data=documentary_topics,
            meta=page_info
        )


    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a documentary topic exists based on the provided criteria.

        Args:
            **kwargs: Field-value pairs to check against

        Returns:
            True if a matching role exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field name is provided
            DatabaseException: If an error occurs during the query
        """
        valid_fields = Ambito.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Ambito model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}"
                )

        stmt = select(Ambito.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Ambito, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None