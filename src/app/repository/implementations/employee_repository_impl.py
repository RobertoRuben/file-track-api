import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IEmployeeRepository
from src.app.model.entity import Trabajador, Cargo, Area
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination

from src.app.schema import Page


class EmployeeRepositoryImpl(IEmployeeRepository):

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, trabajador: Trabajador) -> Trabajador:
        """
        Save an employee entity to the database.

        Args:
            trabajador: The employee entity to save

        Returns:
            The persisted employee with updated attributes

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        self.session.add(trabajador)
        return trabajador

    @transactional(readonly=True)
    async def get_all(self) -> list[Trabajador]:
        """
        Retrieve all employees from the database.

        Returns:
            A list containing all employees

        Raises:
            DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Trabajador)
        results = await self.session.exec(stmt)
        employees = results.all()
        return list(employees)

    @transactional(readonly=False)
    async def delete(self, trabajador_id: int) -> bool:
        """
        Delete an employee from the database by ID.

        Args:
            trabajador_id: The ID of the employee to delete

        Returns:
            True if the employee was successfully deleted, False otherwise

        Raises:
            EntityNotFoundException: If the employee does not exist
            DatabaseException: If an error occurs during the deletion
        """
        employee = await self.get_by_id(trabajador_id)
        await self.session.delete(employee)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, trabajador_id: int) -> Trabajador:
        """
        Retrieve an employee from the database by ID.

        Args:
            trabajador_id: The ID of the employee to retrieve

        Returns:
            The employee entity if found

        Raises:
            EntityNotFoundException: If the employee does not exist
            DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Trabajador).where(Trabajador.id == trabajador_id)
        results = await self.session.exec(stmt)
        employee = results.first()
        return employee

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of employees.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page

        Returns:
            A Page object containing employees and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the retrieval
        """
        offset_value = (page - 1) * size
        stmt = (
            select(
                Trabajador.id.label("id"),
                Trabajador.dni.label("dni"),
                Trabajador.nombres,
                Trabajador.apellido_paterno,
                Trabajador.apellido_materno,
                Trabajador.genero,
                Trabajador.cargo_id,
                Cargo.nombre.label("cargo_nombre"),
                Trabajador.area_id,
                Area.nombre.label("area_nombre"),
                Trabajador.created_at,
                Trabajador.updated_at,
            )
            .join(Area, Area.id == Trabajador.area_id)
            .join(Cargo, Cargo.id == Trabajador.cargo_id)
        )

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        employees_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Trabajador.id))
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
            data=employees_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search employees with filtering and pagination, case-insensitive.

        Args:
            page: Page number (1-based indexing)
            size: Number of items per page
            search_dict: Dictionary of field-value pairs to search for

        Returns:
            A Page object containing the filtered employees and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the search operation
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["nombres", "dni", "apellido_paterno", "apellido_materno"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "dni":
                try:
                    dni_value = int(search_value)
                    conditions.append(Trabajador.dni == dni_value)
                except ValueError:
                    conditions.append(
                        func.cast(Trabajador.dni, func.text('text')).like(
                            f"{search_value}%"
                        )
                    )
            else:
                normalized_search = search_value.lower()

                if field_name == "nombres":
                    field = Trabajador.nombres
                elif field_name == "apellido_paterno":
                    field = Trabajador.apellido_paterno
                elif field_name == "apellido_materno":
                    field = Trabajador.apellido_materno

                conditions.append(func.lower(field) == normalized_search)
                conditions.append(func.lower(field).like(f"{normalized_search}%"))
                conditions.append(func.lower(field).like(f"%{normalized_search}%"))

        stmt = (
            select(
                Trabajador.id.label("id"),
                Trabajador.dni.label("dni"),
                Trabajador.nombres,
                Trabajador.apellido_paterno,
                Trabajador.apellido_materno,
                Trabajador.genero,
                Trabajador.cargo_id,
                Cargo.nombre.label("cargo_nombre"),
                Trabajador.area_id,
                Area.nombre.label("area_nombre"),
                Trabajador.created_at,
                Trabajador.updated_at,
            )
            .join(Area, Area.id == Trabajador.area_id)
            .join(Cargo, Cargo.id == Trabajador.cargo_id)
        )

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        employees_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Trabajador.id))

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
            data=employees_data,
            meta=pagination_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if an employee exists based on the provided criteria.

        Args:
            **kwargs: Field-value pairs to check against

        Returns:
            True if a matching employee exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field name is provided
            DatabaseException: If an error occurs during the query
        """
        valid_fields = Trabajador.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Trabajador model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Trabajador.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Trabajador, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None
