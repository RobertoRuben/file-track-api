import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IComunicacionAreaRepository
from src.app.model.entity import ComunicacionArea, Area
from src.app.exception.invalid_field_exception import InvalidFieldException
from src.app.schema import Page, Pagination


class ComunicationDepartmentRepositoryImpl(IComunicacionAreaRepository):
    """
    Repository implementation for handling ComunicacionArea entities.
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
    async def save(self, comunicacion_area: ComunicacionArea) -> ComunicacionArea:
        """
        Save a communication between areas to the database.

        Args:
            comunicacion_area: The communication between areas to save

        Returns:
            The saved communication between areas with updated data
        """
        self.session.add(comunicacion_area)
        return comunicacion_area

    @transactional(readonly=True)
    async def get_all(self) -> list[ComunicacionArea]:
        """
        Retrieve all communications between areas from the database.

        Returns:
            A list containing all communications between areas
        """
        stmt = select(ComunicacionArea)
        results = await self.session.exec(stmt)
        comunicaciones = results.all()
        return list(comunicaciones)

    @transactional(readonly=False)
    async def delete(self, comunicacion_area_id: int) -> bool:
        """
        Delete a communication between areas by its ID.

        Args:
            comunicacion_area_id: The ID of the communication between areas to delete

        Returns:
            True if the communication was successfully deleted, False otherwise
        """
        comunicacion = await self.get_by_id(comunicacion_area_id)
        await self.session.delete(comunicacion)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, comunicacion_area_id: int) -> ComunicacionArea:
        """
        Retrieve a communication between areas by its ID.

        Args:
            comunicacion_area_id: The ID of the communication between areas to retrieve

        Returns:
            The found communication between areas
        """
        stmt = select(ComunicacionArea).where(
            ComunicacionArea.id == comunicacion_area_id
        )
        results = await self.session.exec(stmt)
        comunicacion = results.first()
        return comunicacion

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of communications between areas.

        Args:
            page: The page number (starts at 1)
            size: The size of each page

        Returns:
            A Page object containing communications between areas and pagination information
        """
        offset = (page - 1) * size
        stmt = (
            select(
                ComunicacionArea.id,
                ComunicacionArea.area_origen_id,
                ComunicacionArea.area_destino_id,
                ComunicacionArea.created_at,
                ComunicacionArea.updated_at,
                Area.nombre.label("area_origen_nombre"),
            )
            .join(Area, Area.id == ComunicacionArea.area_origen_id)
            .add_columns(
                select(Area.nombre)
                .where(Area.id == ComunicacionArea.area_destino_id)
                .scalar_subquery()
                .label("area_destino_nombre")
            )
        )

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        comunicaciones_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(ComunicacionArea.id))
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
            data=comunicaciones_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Search for communications between areas according to search criteria.

        Args:
            page: The page number (starts at 1)
            size: The size of each page
            search_dict: Dictionary containing search parameters

        Returns:
            A Page object with communications between areas that match the search criteria
        """
        offset = (page - 1) * size
        conditions = []

        allowed_fields = ["area_origen_id", "area_destino_id"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name in ["area_origen_id", "area_destino_id"]:
                try:
                    area_id = int(search_value)
                    if field_name == "area_origen_id":
                        conditions.append(ComunicacionArea.area_origen_id == area_id)
                    else:
                        conditions.append(ComunicacionArea.area_destino_id == area_id)
                except ValueError:
                    continue

        stmt = (
            select(
                ComunicacionArea.id,
                ComunicacionArea.area_origen_id,
                ComunicacionArea.area_destino_id,
                ComunicacionArea.created_at,
                ComunicacionArea.updated_at,
                Area.nombre.label("area_origen_nombre"),
            )
            .join(Area, Area.id == ComunicacionArea.area_origen_id)
            .add_columns(
                select(Area.nombre)
                .where(Area.id == ComunicacionArea.area_destino_id)
                .scalar_subquery()
                .label("area_destino_nombre")
            )
        )

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        comunicaciones_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(ComunicacionArea.id))

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
            data=comunicaciones_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if a communication between areas exists according to given criteria.

        Args:
            **kwargs: Key-value pairs representing the search criteria

        Returns:
            True if a matching communication between areas exists, False otherwise
        """
        valid_fields = ComunicacionArea.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the ComunicacionArea model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(ComunicacionArea.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(ComunicacionArea, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None
