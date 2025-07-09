import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.core.db.decorator import transactional
from src.app.repository.interfaces import IHamletRepository
from src.app.model.entity import Hamlet, Settlement
from src.app.core.exception import InvalidFieldException
from src.app.core.schema import Page, Pagination


class HamletRepositoryImpl(IHamletRepository):
    """
    HamletRepositoryImpl is a concrete implementation of the IHamletRepository interface.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, hamlet: Hamlet) -> Hamlet:
        """
        Save a hamlet entity to the database.

        :param hamlet: The hamlet entity to save
        :return: The persisted hamlet with updated attributes
        :raises DatabaseException: If an error occurs during the save operation
        """
        self.session.add(hamlet)
        return hamlet

    @transactional(readonly=True)
    async def get_all(self) -> list[Hamlet]:
        """
        Retrieve all hamlets from the database.

        :return: A list containing all hamlets
        :raises DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Hamlet)
        results = await self.session.exec(stmt)
        hamlets = results.all()
        return list(hamlets)

    @transactional(readonly=False)
    async def delete(self, hamlet_id: int) -> bool:
        """
        Delete a hamlet from the database by ID.

        :param hamlet_id: The ID of the hamlet to delete
        :return: True if the deletion was successful, False otherwise
        :raises DatabaseException: If an error occurs during the deletion
        """
        hamlet = await self.get_by_id(hamlet_id)
        await self.session.delete(hamlet)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, hamlet_id: int) -> Hamlet:
        """
        Retrieve a hamlet from the database by ID.

        :param hamlet_id: The ID of the hamlet to retrieve
        :return: The hamlet entity with the specified ID
        :raises EntityNotFoundException: If the hamlet does not exist
        :raises DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Hamlet).where(Hamlet.id == hamlet_id)
        results = await self.session.exec(stmt)
        hamlet = results.first()
        return hamlet

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of hamlets.

        :param page: The page number to retrieve
        :param size: The number of items per page
        :return: A Page object containing the paginated results
        :raises DatabaseException: If an error occurs during the retrieval
        """
        offset_value = (page - 1) * size
        stmt = select(
            Hamlet.id,
            Hamlet.name,
            Hamlet.settlement_id,
            Settlement.name.label("settlement_name"),
            Hamlet.created_at,
            Hamlet.updated_at,
        ).join(Settlement, Hamlet.settlement_id == Settlement.id, isouter=True)

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        hamlets_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Hamlet.id))
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
            data=hamlets_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Retrieve a paginated list of hamlets based on search criteria.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :param search_dict: Dictionary containing search criteria
        :return: A Page object containing hamlets and pagination metadata
        :raises InvalidFieldException: If an invalid search field is provided
        :raises DatabaseException: If an error occurs during the retrieval
        """

        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["name"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "name":
                field = Hamlet.name

            conditions.append(func.lower(field).like(f"%{search_value.lower()}%"))

        stmt = select(
            Hamlet.id,
            Hamlet.name,
            Hamlet.settlement_id,
            Settlement.name.label("settlement_name"),
            Hamlet.created_at,
            Hamlet.updated_at,
        ).join(Settlement, Hamlet.settlement_id == Settlement.id, isouter=True)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        hamlets_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Hamlet.id))

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

        :param kwargs: Criteria for checking existence
        :return: True if the hamlet exists, False otherwise
        :raises InvalidFieldException: If an invalid field is provided
        :raises DatabaseException: If an error occurs during the check
        """
        valid_fields = Hamlet.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Hamlet model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Hamlet.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Hamlet, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=False)
    async def delete_by_ids(self, hamlet_ids: list[int]) -> bool:
        """
        Delete multiple hamlets from the database by their IDs.

        :param hamlet_ids: List of hamlet IDs to delete
        :return: True if all hamlets were deleted successfully, False otherwise
        :raises DatabaseException: If an error occurs during deletion
        """
        stmt = select(Hamlet).where(Hamlet.id.in_(hamlet_ids))
        results = await self.session.exec(stmt)
        hamlets = results.all()

        found_ids = {hamlet.id for hamlet in hamlets}
        if len(found_ids) != len(hamlet_ids):
            return False

        for hamlet in hamlets:
            await self.session.delete(hamlet)

        return True

    @transactional(readonly=True)
    async def find_by_ids(self, hamlet_ids: list[int]) -> list[Hamlet]:
        """
        Retrieve hamlets by a list of IDs with settlement information.

        :param hamlet_ids: List of hamlet IDs to retrieve
        :return: List of hamlets matching the provided IDs
        :raises DatabaseException: If an error occurs during retrieval
        """
        if not hamlet_ids:
            return []

        stmt = (
            select(Hamlet)
            .join(Settlement, Hamlet.settlement_id == Settlement.id, isouter=True)
            .where(Hamlet.id.in_(hamlet_ids))
        )

        results = await self.session.exec(stmt)
        hamlets = list(results.all())
        return hamlets
