import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.core.db.decorator import transactional
from src.app.repository.interfaces import ISettlementRepository
from src.app.model.entity import Settlement
from src.app.core.exception import InvalidFieldException
from src.app.core.schema import Page, Pagination


class SettlementRepositoryImpl(ISettlementRepository):

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, settlement: Settlement) -> Settlement:
        """
        Save a settlement entity to the database.

        :param settlement: The Settlement entity to save
        :return: The persisted Settlement with updated attributes
        :raises: DatabaseException if an error occurs during the save operation
        """
        self.session.add(settlement)
        return settlement

    @transactional(readonly=True)
    async def get_all(self) -> list[Settlement]:
        """
        Retrieve all settlement entities from the database.

        :return: A list of all Settlement entities
        :raises: DatabaseException if an error occurs while retrieving settlements
        """
        stmt = select(Settlement)
        results = await self.session.exec(stmt)
        settlements = results.all()
        return list(settlements)

    @transactional(readonly=False)
    async def delete(self, settlement_id: int) -> bool:
        """
        Delete a settlement entity by its ID.

        :param settlement_id: The ID of the settlement to delete
        :return: True if the deletion was successful
        :raises: DatabaseException if an error occurs during deletion
        """
        settlement = await self.get_by_id(settlement_id)
        await self.session.delete(settlement)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, settlement_id: int) -> Settlement:
        """
        Retrieve a settlement entity by its ID.

        :param settlement_id: The ID of the settlement to retrieve
        :return: The Settlement entity with the given ID
        :raises: DatabaseException if an error occurs during retrieval
        """
        stmt = select(Settlement).where(Settlement.id == settlement_id)
        results = await self.session.exec(stmt)
        settlement = results.first()
        return settlement

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve settlements with pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :return: A Page object containing the settlements and pagination metadata
        :raises: DatabaseException if an error occurs during the paginated query
        """
        offset_value = (page - 1) * size
        stmt = select(Settlement)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        settlements = list(results.all())

        count_stmt = select(func.count(Settlement.id))
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

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :param search_dict: Dictionary of field-value pairs to search for
        :return: A Page object containing the filtered settlements and pagination metadata
        :raises: DatabaseException if an error occurs during the search operation
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["name"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "name":
                normalized_search = search_value.lower()
                conditions.append(
                    func.lower(Settlement.name).like(f"%{normalized_search}%")
                )

        stmt = select(Settlement)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        settlements = list(results.all())

        count_stmt = select(func.count(Settlement.id))

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

        :param kwargs: Field-value pairs to check against
        :return: True if a matching settlement exists, False otherwise
        :raises InvalidFieldException: If an invalid field name is provided
        :raises DatabaseException: If an error occurs during the query
        """
        valid_fields = Settlement.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Settlement model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Settlement.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Settlement, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=True)
    async def delete_by_ids(self, settlement_ids: list[int]) -> bool:
        """
        Deletes multiple settlement entities from the database by their IDs.

        :param settlement_ids: List of settlement IDs to delete
        :return: True if all settlements were successfully deleted, False otherwise
        """
        stmt = select(Settlement).where(Settlement.id.in_(settlement_ids))
        results = await self.session.exec(stmt)
        settlements = results.all()

        founds_ids = {settlement.id for settlement in settlements}

        if len(founds_ids) != len(settlement_ids):
            raise False
        for settlement in settlements:
            await self.session.delete(settlement)
        return True

    @transactional(readonly=False)
    async def find_by_ids(self, settlement_ids: list[int]) -> list[Settlement]:
        """
        Retrieves multiple settlement entities from the database by their IDs.

        :param settlement_ids: List of settlement IDs to retrieve
        :return: List of Settlement entities with the given IDs
        :raises DatabaseException: If an error occurs during the retrieval
        """
        if not settlement_ids:
            return []

        stmt = select(Settlement).where(Settlement.id.in_(settlement_ids))
        results = await self.session.exec(stmt)
        settlements = results.all()

        return list(settlements)
