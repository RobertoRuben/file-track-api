import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IAreaRepository
from src.app.model.entity import Area, area
from src.app.exception.invalid_field_exception import InvalidFieldException
from src.app.schema import Page, Pagination

class AreaRepositoryImpl(IAreaRepository):
    """
    Repository implementation for handling Area entities.
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
    async def save(self, area: Area) -> Area:
        """
        Save an area entity to the database.

        Args:
            area: The Area entity to save

        Returns:
            The persisted Area with updated attributes

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        self.session.add(area)
        return area

    @transactional(readonly=True)
    async def get_all(self) -> list[Area]:
        """
        Retrieve all area entities from the database.

        Returns:
            A list of all Area entities

        Raises:
            DatabaseException: If an error occurs while retrieving areas
        """
        stmt = select(Area)
        results = await self.session.exec(stmt)
        areas = results.all()
        return list(areas)

    @transactional(readonly=False)
    async def delete(self, area_id: int) -> bool:
        """
        Delete an area entity by its ID.

        Args:
            area_id: The ID of the area to delete

        Returns:
            True if the deletion was successful

        Raises:
            DatabaseException: If an error occurs during deletion
        """
        rol = await self.get_by_id(area_id)
        await self.session.delete(rol)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, area_id: int) -> Area:
        """
        Retrieve an area entity by its ID.

        Args:
            area_id: The ID of the area to retrieve

        Returns:
            The Area entity with the given ID

        Raises:
            DatabaseException: If an error occurs during retrieval
        """
        stmt = select(Area).where(Area.id == area_id)
        results = await self.session.exec(stmt)
        rol = results.first()
        return rol

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve areas with pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page

        Returns:
            A Page object containing the areas and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the paginated query
        """
        offset = (page - 1) * size
        stmt = select(Area)
        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        areas = list(results.all())

        count_stmt = select(func.count(Area.id))
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
            data=areas,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for areas with filtering and pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page
            search_dict: Dictionary of field-value pairs to search for

        Returns:
            A Page object containing the filtered areas and pagination metadata

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
                conditions.append(func.lower(Area.nombre).like(f"%{normalized_search}%"))

        stmt = select(Area)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        areas = list(results.all())

        count_stmt = select(func.count(Area.id))

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
            data=areas,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if an area exists based on the provided criteria.

        Args:
            **kwargs: Field-value pairs to check against

        Returns:
            True if a matching area exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field name is provided
            DatabaseException: If an error occurs during the query
        """
        valid_fields = Area.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Area model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}"
                )

        stmt = select(Area.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Area, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None