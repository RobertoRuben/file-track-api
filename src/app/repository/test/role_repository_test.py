import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import RoleRepositoryImpl
from src.app.model.entity import Role
from src.app.exception import DatabaseException, InvalidFieldException
from src.app.schema import Page, Pagination


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def role_repository(mock_session):
    return RoleRepositoryImpl(session=mock_session)


@pytest.fixture
def role_sample():
    return Role(id=1, name="Administrator", created_at=datetime.now(), updated_at=None)


class TestRoleRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(self, role_repository, mock_session, role_sample):
        """
        Test to verify that the save method correctly stores a role.
        """
        print("🧪 Testing successful role saving...")

        result = await role_repository.save(role_sample)

        mock_session.add.assert_called_once_with(role_sample)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(role_sample)
        assert result == role_sample
        print(f"✅ Role saved successfully: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, role_repository, mock_session, role_sample
    ):
        """
        Test to verify that the save method correctly handles integrity errors.
        """
        print("🧪 Testing integrity error handling during save...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError(
            "Duplicate entry", None, error_original
        )

        with pytest.raises(DatabaseException) as exc_info:
            await role_repository.save(role_sample)

        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, role_repository, mock_session):
        """
        Test to verify that get_all returns all roles.
        """
        print("🧪 Testing retrieval of all roles...")

        roles = [Role(id=1, name="Administrator"), Role(id=2, name="User")]

        role_repository.get_all = AsyncMock(return_value=roles)

        result = await role_repository.get_all()

        assert len(result) == 2
        assert result[0].name == "Administrator"
        assert result[1].name == "User"
        print(f"✅ All roles retrieved: {len(result)} roles found")
        for i, role in enumerate(result):
            print(f"   - Role {i + 1}: ID={role.id}, Name='{role.name}'")

    @pytest.mark.asyncio
    async def test_delete_success(self, role_repository, mock_session, role_sample):
        """
        Test to verify that delete correctly removes a role.
        """
        print("🧪 Testing role deletion...")

        role_repository.get_by_id = AsyncMock(return_value=role_sample)

        result = await role_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(role_sample)
        mock_session.commit.assert_called_once()
        print(f"✅ Role deleted successfully: ID=1, Name='{role_sample.name}'")

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, role_repository, mock_session, role_sample):
        """
        Test to verify that get_by_id returns the correct role.
        """
        print("🧪 Testing role retrieval by ID...")

        role_repository.get_by_id = AsyncMock(return_value=role_sample)

        result = await role_repository.get_by_id(1)

        assert result == role_sample
        assert result.name == "Administrator"
        print(f"✅ Role retrieved by ID: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, role_repository, mock_session):
        """
        Test to verify that get_pageable returns a page of results.
        """
        print("🧪 Testing role pagination...")

        roles = [Role(id=1, name="Administrator"), Role(id=2, name="User")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=roles, meta=pagination_info)

        role_repository.get_pageable = AsyncMock(return_value=page)

        result = await role_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Roles paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} roles"
        )
        for i, role in enumerate(result.data):
            print(f"   - Role {i + 1}: ID={role.id}, Name='{role.name}'")

    @pytest.mark.asyncio
    async def test_exists_by_success(self, role_repository, mock_session):
        """
        Test to verify that exists_by returns True when the role exists.
        """
        print("🧪 Testing role existence verification...")

        role_repository.exists_by = AsyncMock(return_value=True)

        result = await role_repository.exists_by(name="Administrator")

        assert result is True
        print(f"✅ Role existence verified: 'Administrator' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, role_repository, mock_session):
        """
        Test to verify that exists_by returns False when the role doesn't exist.
        """
        print("🧪 Testing non-existent role verification...")

        role_repository.exists_by = AsyncMock(return_value=False)

        result = await role_repository.exists_by(name="Non-existent Role")

        assert result is False
        print(f"✅ Role non-existence verified: 'Non-existent Role' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, role_repository):
        """
        Test to verify that exists_by throws an exception with invalid field.
        """
        print("🧪 Testing invalid field handling...")

        role_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException("Invalid field")
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await role_repository.exists_by(non_existent_field="value")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, role_repository, mock_session):
        """
        Test to verify that find correctly filters by search criteria.
        """
        print("🧪 Testing search with filters...")

        roles = [Role(id=1, name="Administrator")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=roles, meta=pagination_info)

        role_repository.find = AsyncMock(return_value=page)

        search_params = {"name": "admin"}
        result = await role_repository.find(page=1, size=10, search_dict=search_params)

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].name == "Administrator"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, role in enumerate(result.data):
            print(f"   - Result {i + 1}: ID={role.id}, Name='{role.name}'")
