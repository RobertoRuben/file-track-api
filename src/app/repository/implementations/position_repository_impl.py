import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IPositionRepository
from src.app.model.entity import Position
from src.app.exception.invalid_field_exception import InvalidFieldException
from src.app.schema import Page, Pagination


class PositionRepositoryImpl(IPositionRepository):
    """
    Repository implementation for handling Position entities.
    Provides methods for CRUD operations and search functionality.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, position: Position) -> Position:
        """
        Save a position entity to the database.

        :param position: The position entity to save
        :return: The saved position with updated data

        :raises DatabaseException: If an error occurs during the save operation
        """
        self.session.add(position)
        return position

    @transactional(readonly=True)
    async def get_all(self) -> list[Position]:
        """
        Retrieve all position entities from the database.

        :return: A list containing all positions

        :raises DatabaseException: If an error occurs while retrieving positions
        """
        stmt = select(Position)
        results = await self.session.exec(stmt)
        positions = results.all()
        return list(positions)

    @transactional(readonly=False)
    async def delete(self, position_id: int) -> bool:
        """
        Delete a position entity from the database by its ID.

        :param position_id: The ID of the position to delete
        :return: True if the position was successfully deleted, False otherwise

        :raises DatabaseException: If an error occurs during deletion
        """
        position = await self.get_by_id(position_id)
        await self.session.delete(position)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, position_id: int) -> Position:
        """
        Retrieve a position entity from the database by its ID.

        :param position_id: The ID of the position to retrieve
        :return: The found position entity

        :raises DatabaseException: If an error occurs during retrieval
        """
        stmt = select(Position).where(Position.id == position_id)
        results = await self.session.exec(stmt)
        position = results.first()
        return position

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of position entities from the database.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing positions and pagination information

        :raises DatabaseException: If an error occurs during the paginated query
        """
        offset = (page - 1) * size
        stmt = select(Position)
        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        positions = list(results.all())

        count_stmt = select(func.count(Position.id))
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
            data=positions,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Retrieve a paginated list of position entities based on search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with positions matching the search criteria

        :raises DatabaseException: If an error occurs during the search operation
        """
        offset = (page - 1) * size
        conditions = []

        allowed_fields = ["name"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "name":
                normalized_search = search_value.lower()
                conditions.append(
                    func.lower(Position.name).like(f"%{normalized_search}%")
                )

        stmt = select(Position)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        positions = list(results.all())

        count_stmt = select(func.count(Position.id))

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
            data=positions,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a position entity exists in the database based on specific criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching position exists, False otherwise

        :raises InvalidFieldException: If an invalid field name is provided
        :raises DatabaseException: If an error occurs during the query
        """
        valid_fields = Position.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Position model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Position.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Position, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=False)
    async def delete_by_ids(self, position_ids: list[int]) -> bool:
        """
        Elimina múltiples posiciones de la base de datos por sus IDs.

        :param position_ids: Lista de IDs de posiciones a eliminar
        :return: True si todas las posiciones fueron eliminadas correctamente, False en caso contrario
        :raises: DatabaseException si ocurre un error durante la eliminación
        """
        stmt = select(Position).where(Position.id.in_(position_ids))
        results = await self.session.exec(stmt)
        positions = results.all()

        found_ids = {position.id for position in positions}
        if len(found_ids) != len(position_ids):
            return False

        for position in positions:
            await self.session.delete(position)

        return True

    @transactional(readonly=True)
    async def find_by_ids(self, position_ids: list[int]) -> list[Position]:
        """
        Busca posiciones por una lista de IDs.

        :param position_ids: Lista de IDs de posiciones a recuperar
        :return: Lista de posiciones que coinciden con los IDs proporcionados
        :raises: DatabaseException si ocurre un error durante la recuperación
        """
        if not position_ids:
            return []

        stmt = select(Position).where(Position.id.in_(position_ids))
        results = await self.session.exec(stmt)
        positions = list(results.all())
        return positions
