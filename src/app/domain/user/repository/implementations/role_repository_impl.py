import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.core.db.decorator import transactional
from src.app.core.exception import InvalidFieldException
from src.app.core.schema import Page, Pagination
from src.app.domain.user.model import Role
from src.app.domain.user.repository.interface import IRoleRepository


class RoleRepositoryImpl(IRoleRepository):
    """
    Repository implementation for handling Role entities.
    Provides methods for CRUD operations and search functionality.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, rol: Role) -> Role:
        """
        Save a role entity to the database.

        :param rol: The Role entity to save
        :return: The persisted Role with updated attributes
        :raises: DatabaseException if an error occurs during the save operation
        """
        self.session.add(rol)
        return rol

    @transactional(readonly=True)
    async def get_all(self) -> list[Role]:
        """
        Retrieve all role entities from the database.

        :return: A list of all Role entities
        :raises: DatabaseException if an error occurs while retrieving roles
        """
        stmt = select(Role)
        results = await self.session.exec(stmt)
        roles = results.all()
        return list(roles)

    @transactional(readonly=False)
    async def delete(self, rol_id: int) -> bool:
        """
        Delete a role entity by its ID.

        :param rol_id: The ID of the role to delete
        :return: True if the deletion was successful
        :raises: DatabaseException if an error occurs during deletion
        """
        rol = await self.get_by_id(rol_id)
        await self.session.delete(rol)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, rol_id: int) -> Role:
        """
        Retrieve a role entity by its ID.

        :param rol_id: The ID of the role to retrieve
        :return: The Role entity with the given ID
        :raises: DatabaseException if an error occurs during retrieval
        """
        stmt = select(Role).where(Role.id == rol_id)
        results = await self.session.exec(stmt)
        rol = results.first()
        return rol

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve roles with pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :return: A Page object containing the roles and pagination metadata
        :raises: DatabaseException if an error occurs during the paginated query
        """
        offset_value = (page - 1) * size
        stmt = select(Role).order_by(Role.id)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        roles = list(results.all())

        count_stmt = select(func.count(Role.id))
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
            data=roles,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for roles with filtering and pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :param search_dict: Dictionary of field-value pairs to search for
        :return: A Page object containing the filtered roles and pagination metadata
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
                conditions.append(func.lower(Role.name).like(f"%{normalized_search}%"))

        stmt = select(Role)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        roles = list(results.all())

        count_stmt = select(func.count(Role.id))

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

        return Page(data=roles, meta=page_info)

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a role exists based on the provided criteria.

        :param kwargs: Field-value pairs to check against
        :return: True if a matching role exists, False otherwise
        :raises: InvalidFieldException if an invalid field name is provided
        :raises: DatabaseException if an error occurs during the query
        """
        valid_fields = Role.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Role model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Role.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Role, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=False)
    async def delete_by_ids(self, rol_ids: list[int]) -> bool:
        """
        Delete multiple role entities from the database by their IDs.

        :param rol_ids: List of role IDs to delete
        :return: True if all roles were successfully deleted, False otherwise
        :raises: DatabaseException if an error occurs during deletion
        """
        stmt = select(Role).where(Role.id.in_(rol_ids))
        results = await self.session.exec(stmt)
        roles = results.all()

        found_ids = {role.id for role in roles}
        if len(found_ids) != len(rol_ids):
            return False
        for role in roles:
            await self.session.delete(role)

        return True

    @transactional(readonly=True)
    async def find_by_ids(self, role_ids: list[int]) -> list[Role]:
        """
        Find roles by a list of IDs.

        :param role_ids: List of role IDs to retrieve
        :return: List of roles matching the provided IDs
        :raises: DatabaseException if an error occurs during retrieval
        """
        if not role_ids:
            return []

        stmt = select(Role).where(Role.id.in_(role_ids))
        results = await self.session.exec(stmt)
        roles = list(results.all())
        return roles
