import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import ISettlementRepository
from src.app.model.entity import CentroPoblado
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination


class SettlementRepositoryImpl(ISettlementRepository):

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, settlement: CentroPoblado) -> CentroPoblado:
        """
        Save a settlement entity to the database.

        Args:
            settlement: The CentroPoblado entity to save

        Returns:
            The persisted CentroPoblado with updated attributes

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        self.session.add(settlement)
        return settlement

    @transactional(readonly=True)
    async def get_all(self) -> list[CentroPoblado]:
        """
        Retrieve all settlement entities from the database.

        Returns:
            A list of all CentroPoblado entities

        Raises:
            DatabaseException: If an error occurs while retrieving settlements
        """
        stmt = select(CentroPoblado)
        results = await self.session.exec(stmt)
        settlements = results.all()
        return list(settlements)

    @transactional(readonly=False)
    async def delete(self, settlement_id: int) -> bool:
        """
        Delete a settlement entity by its ID.

        Args:
            settlement_id: The ID of the settlement to delete

        Returns:
            True if the deletion was successful

        Raises:
            DatabaseException: If an error occurs during deletion
        """
        settlement = await self.get_by_id(settlement_id)
        await self.session.delete(settlement)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, settlement_id: int) -> CentroPoblado:
        """
        Retrieve a settlement entity by its ID.

        Args:
            settlement_id: The ID of the settlement to retrieve

        Returns:
            The CentroPoblado entity with the given ID

        Raises:
            DatabaseException: If an error occurs during retrieval
        """
        stmt = select(CentroPoblado).where(CentroPoblado.id == settlement_id)
        results = await self.session.exec(stmt)
        settlement = results.first()
        return settlement

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve settlements with pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page

        Returns:
            A Page object containing the settlements and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the paginated query
        """
        offset_value = (page - 1) * size
        stmt = select(CentroPoblado)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        settlements = list(results.all())

        count_stmt = select(func.count(CentroPoblado.id))
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
            data=settlements,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for settlements with filtering and pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page
            search_dict: Dictionary of field-value pairs to search for

        Returns:
            A Page object containing the filtered settlements and pagination metadata

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
                conditions.append(
                    func.lower(CentroPoblado.nombre).like(f"%{normalized_search}%")
                )

        stmt = select(CentroPoblado)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        settlements = list(results.all())

        count_stmt = select(func.count(CentroPoblado.id))

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

        return Page(data=settlements, meta=page_info)

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a settlement exists based on the provided criteria.

        Args:
            **kwargs: Field-value pairs to check against

        Returns:
            True if a matching settlement exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field name is provided
            DatabaseException: If an error occurs during the query
        """
        valid_fields = CentroPoblado.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the CentroPoblado model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(CentroPoblado.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(CentroPoblado, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None
