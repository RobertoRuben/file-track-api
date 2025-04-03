import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IUserRepository
from src.app.model.entity import User, Trabajador, Rol
from src.app.exception import invalid_field_exception
from src.app.schema import Page, Pagination


class UserRepositoryImpl(IUserRepository):
    """
    Repository  implementation for User entity.
    Provides methods for CRUD operations, pagination, and searching.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the UserRepositoryImpl with an AsyncSession.

        Args:
            session (AsyncSession): The SQLAlchemy AsyncSession for database operations.
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, user: User) -> User:
        """
        Saves a new user to the database.

        Args:
            user (User): The User entity to be saved.

        Returns:
            The saved user.
        """
        self.session.add(user)
        return user

    @transactional(readonly=True)
    async def get_all(self) -> list[User]:
        """
        Retrieves all users from the database.

        Returns:
            A list of User.
        """
        stmt = select(User)
        results = await self.session.exec(stmt)
        users = results.all()
        return list(users)

    @transactional(readonly=False)
    async def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: The ID of the user to be deleted.

        Returns:
            True if the user was deleted.
        """
        user = await self.get_by_id(user_id)
        await self.session.delete(user)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by ID.

        Args:
            user_id: The ID of the user to be retrieved.

        Returns:
            The User entity with the specified ID.
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.exec(stmt)
        user = result.first()
        return user

    @transactional(readonly=True)
    async def get_by_username(self, username: str) -> User:
        """
        Retrieves a user by username.

        Args:
            username: The username of the user to retrieve.

        Returns:
            The User entity with the specified username.
        """
        stmt = select(User).where(User.username == username)
        result = await self.session.exec(stmt)
        user = result.first()
        return user

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieves a paginated list of users.

        Args:
            page: The page number to retrieve.
            size: The number of users per page.

        Returns:
            A Page object containing the paginated users.
        """
        offset = (page - 1) * size
        stmt = (
            select(
                User.id,
                User.username,
                User.employee_id,
                func.concat(
                    Trabajador.apellido_paterno,
                    ' ',
                    Trabajador.apellido_materno,
                    ' ',
                    Trabajador.nombres,
                ).label('employee_name'),
                User.is_active,
                User.rol_id,
                Rol.nombre.label("role_name"),
                User.created_at,
                User.updated_at,
            )
            .join(Trabajador, Trabajador.id == User.employee_id)
            .join(Rol, Rol.id == User.rol_id)
        )
        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        users_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(User.id))
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

        Args:
            page: The page number to retrieve.
            size: The number of users per page.
            search_dict: Dictionary containing search criteria (role_name, username, employee_name).

        Returns:
            A Page object containing the paginated users and pagination metadata.
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["role_name", "username", "employee_name"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "username":
                conditions.append(
                    func.lower(User.username).like(f"%{search_value.lower()}%")
                )

            if field_name == "role_name":
                conditions.append(
                    func.lower(Rol.nombre).like(f"%{search_value.lower()}%")
                )

            if field_name == "employee_name":
                conditions.append(
                    func.lower(
                        func.concat(
                            Trabajador.apellido_paterno,
                            ' ',
                            Trabajador.apellido_materno,
                            ' ',
                            Trabajador.nombres,
                        )
                    ).like(f"%{search_value.lower()}%")
                )

        stmt = (
            select(
                User.id,
                User.username,
                User.employee_id,
                func.concat(
                    Trabajador.apellido_paterno,
                    ' ',
                    Trabajador.apellido_materno,
                    ' ',
                    Trabajador.nombres,
                ).label('employee_name'),
                User.is_active,
                User.rol_id,
                Rol.nombre.label("role_name"),
                User.created_at,
                User.updated_at,
            )
            .join(Trabajador, Trabajador.id == User.employee_id)
            .join(Rol, Rol.id == User.rol_id)
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
