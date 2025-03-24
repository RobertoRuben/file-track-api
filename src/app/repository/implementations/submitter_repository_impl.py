import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import ISubmitterRepository
from src.app.model.entity import Remitente
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination


class SubmitterRepositoryImpl(ISubmitterRepository):
    """
    Repository implementation for handling Remitente entities.
    Provides methods for CRUD operations and search functionality.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, remitente: Remitente) -> Remitente:
        """
        Save a sender to the database.

        Args:
            remitente: The Remitente entity to save

        Returns:
            The persisted Remitente with updated attributes

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        self.session.add(remitente)
        return remitente

    @transactional(readonly=True)
    async def get_all(self) -> list[Remitente]:
        """
        Retrieve all senders from the database.

        Returns:
            A list of all Remitente entities

        Raises:
            DatabaseException: If an error occurs while retrieving senders
        """
        stmt = select(Remitente)
        results = await self.session.exec(stmt)
        remitentes = results.all()
        return list(remitentes)

    @transactional(readonly=False)
    async def delete(self, remitente_id: int) -> bool:
        """
        Delete a sender by its ID.

        Args:
            remitente_id: The ID of the sender to delete

        Returns:
            True if the deletion was successful

        Raises:
            DatabaseException: If an error occurs during deletion
        """
        remitente = await self.get_by_id(remitente_id)
        await self.session.delete(remitente)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, remitente_id: int) -> Remitente:
        """
        Retrieve a sender by its ID.

        Args:
            remitente_id: The ID of the sender to retrieve

        Returns:
            The Remitente entity with the given ID

        Raises:
            DatabaseException: If an error occurs during retrieval
        """
        stmt = select(Remitente).where(Remitente.id == remitente_id)
        results = await self.session.exec(stmt)
        remitente = results.first()
        return remitente

    @transactional(readonly=True)
    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Retrieve senders with pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page

        Returns:
            A Page object containing the senders and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the paginated query
        """
        offset_value = (page - 1) * size
        stmt = select(Remitente)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        remitentes = list(results.all())

        count_stmt = select(func.count(Remitente.id))
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

        return Page(data=remitentes, meta=pagination_info)

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search submitters with filtering and pagination, case-insensitive.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page
            search_dict: Dictionary of field-value pairs to search for

        Returns:
            A Page object containing the filtered submitters and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the search operation
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["nombres", "dni", "apellido_paterno", "apellido_materno"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "dni":
                try:
                    dni_value = int(search_value)
                    conditions.append(Remitente.dni == dni_value)
                except ValueError:
                    conditions.append(
                        func.cast(Remitente.dni, func.text('text')).like(
                            f"{search_value}%"
                        )
                    )
            else:
                normalized_search = search_value.lower()

                if field_name == "nombres":
                    field = Remitente.nombres
                elif field_name == "apellido_paterno":
                    field = Remitente.apellido_paterno
                elif field_name == "apellido_materno":
                    field = Remitente.apellido_materno

                conditions.append(func.lower(field) == normalized_search)
                conditions.append(func.lower(field).like(f"{normalized_search}%"))
                conditions.append(
                    func.lower(field).like(f"%{normalized_search}%")
                )  # Contains

        stmt = select(Remitente)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        remitentes = list(results.all())

        count_stmt = select(func.count(Remitente.id))

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

        return Page(data=remitentes, meta=pagination_info)

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a sender exists based on the provided criteria.

        Args:
            **kwargs: Field-value pairs to check against

        Returns:
            True if a matching sender exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field name is provided
            DatabaseException: If an error occurs during the query
        """
        valid_fields = Remitente.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Remitente model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Remitente.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Remitente, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None
