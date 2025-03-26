import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IHamletRepository
from src.app.model.entity import Caserio, CentroPoblado
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination


class HamletRepositoryImpl(IHamletRepository):
    """
    HamletRepositoryImpl is a concrete implementation of the IHamletRepository interface.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, caserio: Caserio) -> Caserio:
        """
        Save a hamlet entity to the database.

        Args:
            caserio: The hamlet entity to save

        Returns:
            The persisted hamlet with updated attributes

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        self.session.add(caserio)
        return caserio

    @transactional(readonly=True)
    async def get_all(self) -> list[Caserio]:
        """
        Retrieve all hamlets from the database.

        Returns:
            A list containing all hamlets

        Raises:
            DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Caserio)
        results = await self.session.exec(stmt)
        hamlets = results.all()
        return list(hamlets)

    @transactional(readonly=False)
    async def delete(self, caserio_id: int) -> bool:
        """
        Delete a hamlet from the database by ID.

        Args:
            caserio_id: The ID of the hamlet to delete

        Returns:
            True if the deletion was successful, False otherwise

        Raises:
            DatabaseException: If an error occurs during the deletion
        """
        hamlet = await self.get_by_id(caserio_id)
        await hamlet.delete(hamlet)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, caserio_id: int) -> Caserio:
        """
        Retrieve a hamlet from the database by ID.

        Args:
            caserio_id: The ID of the hamlet to retrieve

        Returns:
            The hamlet entity with the specified ID

        Raises:
            EntityNotFoundException: If the hamlet does not exist
            DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Caserio).where(Caserio.id == caserio_id)
        results = await self.session.exec(stmt)
        hamlet = results.first()
        return hamlet

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of hamlets.
        Args:
            page: The page number to retrieve
            size: The number of items per page
        Returns:
            A Page object containing the paginated results
        Raises:
            DatabaseException: If an error occurs during the retrieval
        """
        offset_value = (page - 1) * size
        stmt = select(
            Caserio.id,
            Caserio.nombre,
            Caserio.centro_poblado_id,
            CentroPoblado.nombre.label("centro_poblado_nombre"),
            Caserio.created_at,
            Caserio.updated_at,
        ).join(Caserio, on=(Caserio.id == Caserio.id), isouter=True)

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        hamlets_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Caserio.id))
        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1

        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 0 else None

        page_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(
            data=hamlets_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Retrieve a paginated list of hamlets based on search criteria.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page
            search_dict: Dictionary containing search criteria

        Returns:
            A Page object containing hamlets and pagination metadata

        Raises:
            InvalidFieldException: If an invalid search field is provided
            DatabaseException: If an error occurs during the retrieval
        """

        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["nombre"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "nombre":
                field = Caserio.nombre

            conditions.append(func.lower(field).like(f"%{search_value.lower()}%"))

        stmt = select(
            Caserio.id,
            Caserio.nombre,
            Caserio.centro_poblado_id,
            CentroPoblado.nombre.label("centro_poblado_nombre"),
            Caserio.created_at,
            Caserio.updated_at,
        ).join(Caserio, on=(Caserio.id == Caserio.id), isouter=True)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        hamlets_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Caserio.id))

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

        return Page(
            data=hamlets_data,
            meta=pagination_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a hamlet exists based on the provided criteria.

        Args:
            **kwargs: Criteria for checking existence

        Returns:
            True if the hamlet exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field is provided
            DatabaseException: If an error occurs during the check
        """
        valid_fields = Caserio.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Caserio model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Caserio.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Caserio, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None
