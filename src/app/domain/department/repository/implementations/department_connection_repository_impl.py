import math

from sqlalchemy.orm import aliased
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.core.schema import Page, Pagination
from src.app.core.db.decorator import transactional
from src.app.core.exception import InvalidFieldException
from src.app.repository.interfaces import IDepartmentConnectionRepository
from src.app.domain.department.model import DepartmentConnection, Department


class DepartmentConnectionRepositoryImpl(IDepartmentConnectionRepository):
    """
    Repository implementation for handling DepartmentConnection entities.
    Provides methods for CRUD operations and search functionality for department connections.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(
        self, department_connection: DepartmentConnection
    ) -> DepartmentConnection:
        """
        Save a department connection to the database.

        :param department_connection: The department connection to save
        :return: The saved department connection with updated data
        """
        self.session.add(department_connection)
        return department_connection

    @transactional(readonly=True)
    async def get_all(self) -> list[DepartmentConnection]:
        """
        Retrieve all department connections from the database.

        :return: A list containing all department connections
        """
        stmt = select(DepartmentConnection)
        results = await self.session.exec(stmt)
        connections = results.all()
        return list(connections)

    @transactional(readonly=False)
    async def delete(self, department_connection_id: int) -> bool:
        """
        Delete a department connection by its ID.

        :param department_connection_id: The ID of the department connection to delete
        :return: True if the connection was successfully deleted, False otherwise
        """
        connection = await self.get_by_id(department_connection_id)
        await self.session.delete(connection)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, department_connection_id: int) -> DepartmentConnection:
        """
        Retrieve a department connection by its ID.

        :param department_connection_id: The ID of the department connection to retrieve
        :return: The found department connection
        """
        stmt = select(DepartmentConnection).where(
            DepartmentConnection.id == department_connection_id
        )
        results = await self.session.exec(stmt)
        connection = results.first()
        return connection

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of department connections.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing department connections and pagination information
        """
        offset = (page - 1) * size

        SourceDept = aliased(Department, name="source_department")
        TargetDept = aliased(Department, name="target_department")

        stmt = (
            select(
                DepartmentConnection.id,
                DepartmentConnection.source_department_id,
                DepartmentConnection.target_department_id,
                DepartmentConnection.created_at,
                DepartmentConnection.updated_at,
                SourceDept.name.label("source_department_name"),
                TargetDept.name.label("target_department_name"),
            )
            .join(
                SourceDept, SourceDept.id == DepartmentConnection.source_department_id
            )
            .join(
                TargetDept, TargetDept.id == DepartmentConnection.target_department_id
            )
        )

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        connections_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(DepartmentConnection.id))
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
            data=connections_data,
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
        Search for department connections according to search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with department connections that match the search criteria
        """
        offset = (page - 1) * size

        SourceDept = aliased(Department, name="source_department")
        TargetDept = aliased(Department, name="target_department")

        conditions = []

        allowed_fields = [
            "source_department_id",
            "target_department_id",
            "source_department_name",
            "target_department_name",
        ]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name in ["source_department_id", "target_department_id"]:
                try:
                    value = int(search_value)
                    if field_name == "source_department_id":
                        conditions.append(
                            DepartmentConnection.source_department_id == value
                        )
                    else:
                        conditions.append(
                            DepartmentConnection.target_department_id == value
                        )
                except ValueError:
                    pass
            elif field_name == "source_department_name" and search_value:
                conditions.append(SourceDept.name.ilike(f"%{search_value}%"))
            elif field_name == "target_department_name" and search_value:
                conditions.append(TargetDept.name.ilike(f"%{search_value}%"))

        stmt = (
            select(
                DepartmentConnection.id,
                DepartmentConnection.source_department_id,
                DepartmentConnection.target_department_id,
                DepartmentConnection.created_at,
                DepartmentConnection.updated_at,
                SourceDept.name.label("source_department_name"),
                TargetDept.name.label("target_department_name"),
            )
            .join(
                SourceDept, SourceDept.id == DepartmentConnection.source_department_id
            )
            .join(
                TargetDept, TargetDept.id == DepartmentConnection.target_department_id
            )
        )

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        connections_data = [dict(row._mapping) for row in results]

        count_stmt = (
            select(func.count(DepartmentConnection.id))
            .join(
                SourceDept, SourceDept.id == DepartmentConnection.source_department_id
            )
            .join(
                TargetDept, TargetDept.id == DepartmentConnection.target_department_id
            )
        )

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
            data=connections_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if a department connection exists according to given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching department connection exists, False otherwise
        """
        valid_fields = DepartmentConnection.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the DepartmentConnection model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(DepartmentConnection.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(DepartmentConnection, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=True)
    async def get_connections_by_source_department_id(
        self, source_department_id: int
    ) -> list[DepartmentConnection]:
        """
        Gets all department connections by source department ID.

        :param source_department_id: The ID of the source department to filter connections
        :return: A list with all department connections that match the source department ID
        """
        stmt = select(DepartmentConnection).where(
            DepartmentConnection.source_department_id == source_department_id
        )
        results = await self.session.exec(stmt)
        connections = results.all()
        return list(connections)
