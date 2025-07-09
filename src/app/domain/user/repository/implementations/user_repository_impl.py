import math
from typing import Any
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.core.db.decorator import transactional
from src.app.core.exception import invalid_field_exception
from src.app.core.schema import Page, Pagination
from src.app.domain.user.model import User, Role
from src.app.domain.employee.model import Employee
from src.app.domain.department.model import Department
from src.app.domain.user.repository.interface import IUserRepository


class UserRepositoryImpl(IUserRepository):
    """
    Repository implementation for User entity.
    Provides methods for CRUD operations, pagination, and searching.

    :ivar session: The database session used for all operations
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the UserRepositoryImpl with an AsyncSession.

        :param session: The SQLAlchemy AsyncSession for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, user: User) -> User:
        """
        Saves a new user to the database.

        :param user: The User entity to be saved
        :return: The saved user with updated information
        """
        self.session.add(user)
        return user

    @transactional(readonly=True)
    async def get_all(self) -> list[User]:
        """
        Retrieves all users from the database.

        :return: A list of User entities
        """
        stmt = select(User)
        results = await self.session.exec(stmt)
        users = results.all()
        return list(users)

    @transactional(readonly=False)
    async def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        :param user_id: The ID of the user to be deleted
        :return: True if the user was deleted successfully
        """
        user = await self.get_by_id(user_id)
        await self.session.delete(user)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by ID.

        :param user_id: The ID of the user to be retrieved
        :return: The User entity with the specified ID
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.exec(stmt)
        user = result.first()
        return user

    @transactional(readonly=True)
    async def get_by_username(self, username: str) -> User:
        """
        Retrieves a user by username.

        :param username: The username of the user to retrieve
        :return: The User entity with the specified username
        """
        stmt = select(User).where(User.username == username)
        result = await self.session.exec(stmt)
        user = result.first()
        return user

    @transactional(readonly=False)
    async def get_current_user_by_name(self, username: str) -> dict[str, Any] | None:
        """
        Retrieves the current user by username.
        :param username: The username of the user to retrieve
        :return: A dictionary containing user information, or None if not found
        """
        stmt = (
            select(
                User.id,
                User.username,
                User.password,
                func.concat(
                    Employee.paternal_surname,
                    ' ',
                    Employee.maternal_surname,
                    ' ',
                    Employee.names,
                ).label('employee_name'),
                Role.name.label("role_name"),
                Department.id.label("department_id"),
                User.is_active,
                User.created_at,
                User.updated_at,
            )
            .join(Employee, Employee.id == User.employee_id)
            .join(Role, Role.id == User.role_id)
            .join(Department, Department.id == Employee.department_id)
            .where(User.username == username)
        )
        result = await self.session.exec(stmt)
        current_user = result.first()

        return current_user._asdict() if current_user else None

    @transactional(readonly=True)
    async def get_pageable(
        self, page: int, size: int, only_active: bool = True
    ) -> Page:
        """
        Retrieves a paginated list of users, with option to filter by active status.

        :param page: The page number to retrieve
        :param size: The number of users per page
        :param only_active: If True, returns only active users; if False, returns all users
        :return: A Page object containing the paginated users
        """
        offset = (page - 1) * size
        stmt = (
            select(
                User.id,
                User.username,
                User.employee_id,
                func.concat(
                    Employee.paternal_surname,
                    ' ',
                    Employee.maternal_surname,
                    ' ',
                    Employee.names,
                ).label('employee_name'),
                User.is_active,
                User.role_id,
                Role.name.label("role_name"),
                User.created_at,
                User.updated_at,
            )
            .join(Employee, Employee.id == User.employee_id)
            .join(Role, Role.id == User.role_id)
        )

        if only_active:
            stmt = stmt.where(User.is_active == True)
        elif only_active is False:
            stmt = stmt.where(User.is_active == False)

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        users_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(User.id))
        if only_active:
            count_stmt = count_stmt.where(User.is_active == True)
        elif only_active is False:
            count_stmt = count_stmt.where(User.is_active == False)

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
            data=users_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Retrieves a paginated list of users based on search criteria.

        :param page: The page number to retrieve
        :param size: The number of users per page
        :param search_dict: Dictionary containing search criteria (role_name, username, employee_name)
        :return: A Page object containing the paginated users and pagination metadata
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["role_name", "username", "employee_name"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "username":
                conditions.append(User.username.ilike(f"%{search_value}%"))

            if field_name == "role_name":
                conditions.append(Role.name.ilike(f"%{search_value}%"))

            if field_name == "employee_name":
                conditions.append(
                    or_(
                        Employee.names.ilike(f"%{search_value}%"),
                        Employee.paternal_surname.ilike(f"%{search_value}%"),
                        Employee.maternal_surname.ilike(f"%{search_value}%"),
                    )
                )

        stmt = (
            select(
                User.id,
                User.username,
                User.employee_id,
                func.concat(
                    Employee.paternal_surname,
                    ' ',
                    Employee.maternal_surname,
                    ' ',
                    Employee.names,
                ).label('employee_name'),
                User.is_active,
                User.role_id,
                Role.name.label("role_name"),
                User.created_at,
                User.updated_at,
            )
            .join(Employee, Employee.id == User.employee_id)
            .join(Role, Role.id == User.role_id)
        )

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        users_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(User.id))

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
            data=users_data,
            meta=pagination_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Checks if a user exists based on the provided criteria.

        Args:
            **kwargs: Criteria for checking existence.

        Returns:
            True if the user exists, False otherwise.

        Raises:
            InvalidFieldException: If an invalid field is provided
            DatabaseException: If an error occurs during the check
        """
        valid_fields = User.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise invalid_field_exception.InvalidFieldException(
                    message=f"Invalid field '{key} does not exist in the User model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(User.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(User, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=True)
    async def find_by_ids(self, user_ids: list[int]) -> list[User]:
        """
        Retrieve users by a list of IDs with complete information.

        :param user_ids: List of user IDs to retrieve
        :return: List of users matching the provided IDs
        :raises DatabaseException: If an error occurs during retrieval
        """
        if not user_ids:
            return []

        stmt = (
            select(
                User.id,
                User.username,
                User.employee_id,
                func.concat(
                    Employee.paternal_surname,
                    ' ',
                    Employee.maternal_surname,
                    ' ',
                    Employee.names,
                ).label('employee_name'),
                User.is_active,
                User.role_id,
                Role.name.label("role_name"),
                Department.name.label("department_name"),
                User.created_at,
                User.updated_at,
            )
            .join(Employee, Employee.id == User.employee_id)
            .join(Role, Role.id == User.role_id)
            .join(Department, Department.id == Employee.department_id)
            .where(User.id.in_(user_ids))
        )

        results = await self.session.exec(stmt)
        users_data = [dict(row._mapping) for row in results]
        return users_data
