import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.core.db.decorator import transactional
from src.app.core.exception import InvalidFieldException
from src.app.core.schema import Page, Pagination
from src.app.domain.department.model import Department
from src.app.domain.employee.model import Employee, Position
from src.app.domain.employee.repository.interface import IEmployeeRepository


class EmployeeRepositoryImpl(IEmployeeRepository):

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, employee: Employee) -> Employee:
        """
        Save an employee entity to the database.

        :param employee: The employee entity to save
        :return: The persisted employee with updated attributes

        :raises DatabaseException: If an error occurs during the save operation
        """
        self.session.add(employee)
        return employee

    @transactional(readonly=True)
    async def get_all(self) -> list[Employee]:
        """
        Retrieve all employees from the database.

        :return: A list containing all employees

        :raises DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Employee)
        results = await self.session.exec(stmt)
        employees = results.all()
        return list(employees)

    @transactional(readonly=False)
    async def delete(self, employee_id: int) -> bool:
        """
        Delete an employee from the database by ID.

        :param employee_id: The ID of the employee to delete
        :return: True if the employee was successfully deleted, False otherwise

        :raises EntityNotFoundException: If the employee does not exist
        :raises DatabaseException: If an error occurs during the deletion
        """
        employee = await self.get_by_id(employee_id)
        await self.session.delete(employee)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, employee_id: int) -> Employee:
        """
        Retrieve an employee from the database by ID.

        :param employee_id: The ID of the employee to retrieve
        :return: The employee entity if found

        :raises EntityNotFoundException: If the employee does not exist
        :raises DatabaseException: If an error occurs during the retrieval
        """
        stmt = select(Employee).where(Employee.id == employee_id)
        results = await self.session.exec(stmt)
        employee = results.first()
        return employee

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of employees.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :return: A Page object containing employees and pagination metadata

        :raises DatabaseException: If an error occurs during the retrieval
        """
        offset_value = (page - 1) * size
        stmt = (
            select(
                Employee.id.label("id"),
                Employee.dni.label("dni"),
                Employee.names.label("names"),
                Employee.paternal_surname.label("paternal_surname"),
                Employee.maternal_surname.label("maternal_surname"),
                Employee.gender.label("gender"),
                Employee.position_id.label("position_id"),
                Position.name.label("position_name"),
                Employee.department_id.label("department_id"),
                Department.name.label("department_name"),
                Employee.created_at,
                Employee.updated_at,
            )
            .join(Department, Department.id == Employee.department_id)
            .join(Position, Position.id == Employee.position_id)
            .order_by(Employee.id)
        )

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        employees_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Employee.id))
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
            data=employees_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search employees with filtering and pagination, case-insensitive.

        :param page: Page number (1-based indexing)
        :param size: Number of items per page
        :param search_dict: Dictionary of field-value pairs to search for
        :return: A Page object containing the filtered employees and pagination metadata

        :raises DatabaseException: If an error occurs during the search operation
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["names", "dni", "paternal_surname", "maternal_surname"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "dni":
                try:
                    dni_value = int(search_value)
                    conditions.append(Employee.dni == dni_value)
                except ValueError:
                    conditions.append(
                        func.cast(Employee.dni, func.text('text')).like(
                            f"{search_value}%"
                        )
                    )
            else:
                normalized_search = search_value.lower()

                if field_name == "names":
                    field = Employee.names
                elif field_name == "paternal_surname":
                    field = Employee.paternal_surname
                elif field_name == "maternal_surname":
                    field = Employee.maternal_surname

                conditions.append(func.lower(field) == normalized_search)
                conditions.append(func.lower(field).like(f"{normalized_search}%"))
                conditions.append(func.lower(field).like(f"%{normalized_search}%"))

        stmt = (
            select(
                Employee.id.label("id"),
                Employee.dni.label("dni"),
                Employee.names.label("names"),
                Employee.paternal_surname.label("paternal_surname"),
                Employee.maternal_surname.label("maternal_surname"),
                Employee.gender.label("gender"),
                Employee.position_id.label("position_id"),
                Position.name.label("position_name"),
                Employee.department_id.label("department_id"),
                Department.name.label("department_name"),
                Employee.created_at,
                Employee.updated_at,
            )
            .join(Department, Department.id == Employee.department_id)
            .join(Position, Position.id == Employee.position_id)
        )

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        employees_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Employee.id))

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

        :param kwargs: Field-value pairs to check against
        :return: True if a matching employee exists, False otherwise

        :raises InvalidFieldException: If an invalid field name is provided
        :raises DatabaseException: If an error occurs during the query
        """
        valid_fields = Employee.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Employee model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Employee.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Employee, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=False)
    async def delete_by_ids(self, employee_ids: list[int]) -> bool:
        """
        Delete multiple employees from the database by their IDs.

        :param employee_ids: List of employee IDs to delete
        :return: True if all employees were successfully deleted, False otherwise

        :raises DatabaseException: If an error occurs during the deletion
        """
        stmt = select(Employee).where(Employee.id.in_(employee_ids))
        results = await self.session.exec(stmt)
        employees = results.all()

        found_ids = {employee.id for employee in employees}
        if len(found_ids) != len(employee_ids):
            return False

        for employee in employees:
            await self.session.delete(employee)

        return True

    @transactional(readonly=True)
    async def find_by_ids(self, employee_ids: list[int]) -> list[dict]:
        """
        Retrieve multiple employees from the database by their IDs,
        returning the same fields as the get_pageable method.

        :param employee_ids: List of employee IDs to retrieve
        :return: List of employees found with all relevant fields

        :raises DatabaseException: If an error occurs during the retrieval
        """
        if not employee_ids:
            return []

        stmt = (
            select(
                Employee.id.label("id"),
                Employee.dni.label("dni"),
                Employee.names.label("names"),
                Employee.paternal_surname.label("paternal_surname"),
                Employee.maternal_surname.label("maternal_surname"),
                Employee.gender.label("gender"),
                Employee.position_id.label("position_id"),
                Position.name.label("position_name"),
                Employee.department_id.label("department_id"),
                Department.name.label("department_name"),
                Employee.created_at,
                Employee.updated_at,
            )
            .join(Department, Department.id == Employee.department_id)
            .join(Position, Position.id == Employee.position_id)
            .where(Employee.id.in_(employee_ids))
        )

        results = await self.session.exec(stmt)
        employees_data = [dict(row._mapping) for row in results]

        return employees_data
