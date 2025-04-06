import pytest
import math
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import UserRepositoryImpl
from src.app.model.entity import User, Employee, Role
from src.app.exception import DatabaseException, InvalidFieldException
from src.app.schema import Page, Pagination


@pytest.fixture
def mock_session():
    """
    Creates a mock database session for testing.

    :return: A mock AsyncSession object
    """
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def user_repository(mock_session):
    """
    Creates a UserRepositoryImpl instance for testing.

    :param mock_session: The mock database session
    :return: A UserRepositoryImpl instance
    """
    return UserRepositoryImpl(session=mock_session)


@pytest.fixture
def employee_sample():
    """
    Creates a sample Employee entity for testing.

    :return: A sample Employee entity
    """
    return Employee(
        id=1,
        dni=12345678,
        names="Juan Carlos",
        paternal_surname="Pérez",
        maternal_surname="Gómez",
        gender="Male",
        position_id=1,
        area_id=1,
        created_at=datetime.now(),
        updated_at=None,
    )


@pytest.fixture
def role_sample():
    """
    Creates a sample Role entity for testing.

    :return: A sample Role entity
    """
    return Role(id=1, name="Administrator")


@pytest.fixture
def user_sample(employee_sample, role_sample):
    """
    Creates a sample User entity for testing.

    :param employee_sample: A sample Employee entity
    :param role_sample: A sample Role entity
    :return: A sample User entity
    """
    return User(
        id=1,
        username="jperez",
        password="hashed_password",
        employee_id=employee_sample.id,
        role_id=role_sample.id,
        created_at=datetime.now(),
        updated_at=None,
    )


class TestUserRepositoryImpl:
    """
    Test class for UserRepositoryImpl.

    Contains all tests related to user repository operations.
    """

    @pytest.mark.asyncio
    async def test_save_success(self, user_repository, mock_session, user_sample):
        """
        Test to verify that the save method correctly stores a user.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        :param user_sample: A sample User entity
        """
        print("🧪 Testing successful user saving...")

        result = await user_repository.save(user_sample)

        mock_session.add.assert_called_once_with(user_sample)
        assert result == user_sample
        print(
            f"✅ User saved successfully: ID={result.id}, Username='{result.username}'"
        )

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, user_repository, mock_session, user_sample
    ):
        """
        Test to verify that save method correctly handles integrity errors.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        :param user_sample: A sample User entity
        """
        print("🧪 Testing integrity error handling during save...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError(
            "Duplicate entry", None, error_original
        )

        with pytest.raises(DatabaseException) as exc_info:
            await user_repository.save(user_sample)

        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, user_repository, mock_session, user_sample):
        """
        Test to verify that get_all returns all users.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        :param user_sample: A sample User entity
        """
        print("🧪 Testing retrieval of all users...")

        users = [
            user_sample,
            User(
                id=2,
                username="mlopez",
                password="hashed_password",
                employee_id=2,
                role_id=2,
                created_at=datetime.now(),
                updated_at=None,
            ),
        ]

        mock_result = MagicMock()
        mock_result.all.return_value = users
        mock_session.exec.return_value = mock_result

        result = await user_repository.get_all()

        assert len(result) == 2
        assert result[0].username == "jperez"
        assert result[1].username == "mlopez"
        print(f"✅ All users retrieved: {len(result)} users found")
        for i, user in enumerate(result):
            print(f"   - User {i+1}: ID={user.id}, Username='{user.username}'")

    @pytest.mark.asyncio
    async def test_delete_success(self, user_repository, mock_session, user_sample):
        """
        Test to verify that delete successfully removes a user.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        :param user_sample: A sample User entity
        """
        print("🧪 Testing user deletion...")

        user_repository.get_by_id = AsyncMock(return_value=user_sample)

        async def patched_delete(user_id):
            user = await user_repository.get_by_id(user_id)
            await mock_session.delete(user)
            return True

        user_repository.delete = patched_delete

        result = await user_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(user_sample)
        print(f"✅ User deleted successfully: ID=1, Username='{user_sample.username}'")

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, user_repository, mock_session, user_sample):
        """
        Test to verify that get_by_id returns the correct user.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        :param user_sample: A sample User entity
        """
        print("🧪 Testing user retrieval by ID...")

        mock_result = MagicMock()
        mock_result.first.return_value = user_sample
        mock_session.exec.return_value = mock_result

        user_repository.get_by_id = AsyncMock(return_value=user_sample)

        result = await user_repository.get_by_id(1)

        assert result == user_sample
        assert result.username == "jperez"
        print(f"✅ User retrieved by ID: ID={result.id}, Username='{result.username}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, user_repository, mock_session):
        """
        Test to verify that get_pageable returns a page of results.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        """
        print("🧪 Testing user pagination...")

        users_data = [
            {
                "id": 1,
                "username": "jperez",
                "employee_id": 1,
                "employee_name": "Pérez Gómez Juan Carlos",
                "is_active": True,
                "role_id": 1,
                "role_name": "Administrator",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "username": "mlopez",
                "employee_id": 2,
                "employee_name": "López Sánchez María",
                "is_active": True,
                "role_id": 2,
                "role_name": "User",
                "created_at": datetime.now(),
                "updated_at": None,
            },
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=users_data, meta=pagination_info)

        user_repository.get_pageable = AsyncMock(return_value=page)

        result = await user_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        print(
            f"✅ Users paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} users"
        )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, user_repository, mock_session):
        """
        Test to verify that exists_by returns True when the user exists.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        """
        print("🧪 Testing user existence verification...")

        mock_result = AsyncMock()
        mock_result.first.return_value = 1
        mock_session.exec.return_value = mock_result

        result = await user_repository.exists_by(username="jperez")

        assert result is True
        print(
            f"✅ User existence verified: User with username 'jperez' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, user_repository, mock_session):
        """
        Test to verify that exists_by returns False when the user doesn't exist.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        """
        print("🧪 Testing non-existent user verification...")

        user_repository.exists_by = AsyncMock(return_value=False)

        result = await user_repository.exists_by(username="nonexistent")

        assert result is False
        print(
            f"✅ User non-existence verified: User with username 'nonexistent' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, user_repository, mock_session):
        """
        Test to verify that exists_by throws an exception with invalid field.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        """
        print("🧪 Testing invalid field handling...")

        with pytest.raises(InvalidFieldException) as exc_info:
            await user_repository.exists_by(invalid_field="value")

        assert "does not exist in the User model" in str(exc_info.value)
        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, user_repository, mock_session):
        """
        Test to verify that find correctly filters by search criteria.

        :param user_repository: The repository under test
        :param mock_session: The mock database session
        """
        print("🧪 Testing search with filters...")

        users_data = [
            {
                "id": 1,
                "username": "jperez",
                "employee_id": 1,
                "employee_name": "Pérez Gómez Juan Carlos",
                "is_active": True,
                "role_id": 1,
                "role_name": "Administrator",
                "created_at": datetime.now(),
                "updated_at": None,
            }
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=users_data, meta=pagination_info)

        user_repository.find = AsyncMock(return_value=page)

        search_params = {"username": "jperez"}
        result = await user_repository.find(page=1, size=10, search_dict=search_params)

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0]["username"] == "jperez"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, user in enumerate(result.data):
            print(
                f"   - Result {i + 1}: ID={user['id']}, Username='{user['username']}'"
            )
