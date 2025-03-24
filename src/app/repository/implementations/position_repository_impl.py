import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IPositionRepository
from src.app.model.entity import Cargo
from src.app.exception.invalid_field_exception import InvalidFieldException
from src.app.schema import Page, Pagination


class PositionRepositoryImpl(IPositionRepository):
    """
    Repository implementation for handling Cargo (Position) entities.
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
    async def save(self, cargo: Cargo) -> Cargo:
        """
        Save a position entity to the database.

        Args:
            cargo: The position entity to save

        Returns:
            The saved position with updated data

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        self.session.add(cargo)
        return cargo

    @transactional(readonly=True)
    async def get_all(self) -> list[Cargo]:
        """
        Retrieve all position entities from the database.

        Returns:
            A list containing all positions

        Raises:
            DatabaseException: If an error occurs while retrieving positions
        """
        stmt = select(Cargo)
        results = await self.session.exec(stmt)
        cargos = results.all()
        return list(cargos)

    @transactional(readonly=False)
    async def delete(self, cargo_id: int) -> bool:
        """
        Delete a position entity from the database by its ID.

        Args:
            cargo_id: The ID of the position to delete

        Returns:
            True if the position was successfully deleted, False otherwise

        Raises:
            DatabaseException: If an error occurs during deletion
        """
        cargo = await self.get_by_id(cargo_id)
        await self.session.delete(cargo)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, cargo_id: int) -> Cargo:
        """
        Retrieve a position entity from the database by its ID.

        Args:
            cargo_id: The ID of the position to retrieve

        Returns:
            The found position entity

        Raises:
            DatabaseException: If an error occurs during retrieval
        """
        stmt = select(Cargo).where(Cargo.id == cargo_id)
        results = await self.session.exec(stmt)
        cargo = results.first()
        return cargo

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of position entities from the database.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing positions and pagination information

        Raises:
            DatabaseException: If an error occurs during the paginated query
        """
        offset = (page - 1) * size
        stmt = select(Cargo)
        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        cargos = list(results.all())

        count_stmt = select(func.count(Cargo.id))
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
            data=cargos,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Retrieve a paginated list of position entities based on search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with positions matching the search criteria

        Raises:
            DatabaseException: If an error occurs during the search operation
        """
        offset = (page - 1) * size
        conditions = []

        allowed_fields = ["nombre"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "nombre":
                normalized_search = search_value.lower()
                conditions.append(
                    func.lower(Cargo.nombre).like(f"%{normalized_search}%")
                )

        stmt = select(Cargo)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        cargos = list(results.all())

        count_stmt = select(func.count(Cargo.id))

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
            data=cargos,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a position entity exists in the database based on specific criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching position exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field name is provided
            DatabaseException: If an error occurs during the query
        """
        valid_fields = Cargo.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Cargo model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Cargo.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Cargo, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None
