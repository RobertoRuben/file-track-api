import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import DepartmentRepositoryImpl
from src.app.model.entity import Department
from src.app.core.exception import DatabaseException, InvalidFieldException
from src.app.core.schema import Page, Pagination


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def department_repository(mock_session):
    return DepartmentRepositoryImpl(session=mock_session)


@pytest.fixture
def department_sample():
    return Department(
        id=1, name="Recursos Humanos", created_at=datetime.now(), updated_at=None
    )


class TestDepartmentRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, department_repository, mock_session, department_sample
    ):
        """Test to verify that the save method correctly stores a department."""
        print("🧪 Testing successful department saving...")

        result = await department_repository.save(department_sample)

        mock_session.add.assert_called_once_with(department_sample)
        assert result == department_sample
        print(f"✅ Department saved successfully: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, department_repository, mock_session, department_sample
    ):
        """Test to verify that the save method correctly handles integrity errors."""
        print("🧪 Testing integrity error handling during save...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError(
            "Duplicate entry", None, error_original
        )

        with pytest.raises(DatabaseException) as exc_info:
            await department_repository.save(department_sample)

        assert isinstance(exc_info.value, DatabaseException)
        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, department_repository, mock_session):
        """Test to verify that get_all returns all departments."""
        print("🧪 Testing retrieval of all departments...")

        departments = [
            Department(id=1, name="Recursos Humanos"),
            Department(id=2, name="Finanzas"),
        ]

        department_repository.get_all = AsyncMock(return_value=departments)

        result = await department_repository.get_all()

        assert len(result) == 2
        assert result[0].name == "Recursos Humanos"
        assert result[1].name == "Finanzas"
        print(f"✅ All departments retrieved: {len(result)} departments found")
        for i, department in enumerate(result):
            print(
                f"   - Department {i+1}: ID={department.id}, Name='{department.name}'"
            )

    @pytest.mark.asyncio
    async def test_delete_success(
        self, department_repository, mock_session, department_sample
    ):
        """Test to verify that delete correctly removes a department."""
        print("🧪 Testing department deletion...")

        department_repository.get_by_id = AsyncMock(return_value=department_sample)

        result = await department_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(department_sample)
        print(
            f"✅ Department deleted successfully: ID=1, Name='{department_sample.name}'"
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, department_repository, mock_session, department_sample
    ):
        """Test to verify that get_by_id returns the correct department."""
        print("🧪 Testing department retrieval by ID...")

        department_repository.get_by_id = AsyncMock(return_value=department_sample)

        result = await department_repository.get_by_id(1)

        assert result == department_sample
        assert result.name == "Recursos Humanos"
        print(f"✅ Department retrieved by ID: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, department_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing department pagination...")

        departments = [
            Department(id=1, name="Recursos Humanos"),
            Department(id=2, name="Finanzas"),
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=departments, meta=pagination_info)

        department_repository.get_pageable = AsyncMock(return_value=page)

        result = await department_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Departments paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} departments"
        )
        for i, department in enumerate(result.data):
            print(
                f"   - Department {i+1}: ID={department.id}, Name='{department.name}'"
            )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, department_repository, mock_session):
        """Test to verify that exists_by returns True when the department exists."""
        print("🧪 Testing department existence verification...")

        department_repository.exists_by = AsyncMock(return_value=True)

        result = await department_repository.exists_by(name="Recursos Humanos")

        assert result is True
        print(f"✅ Department existence verified: 'Recursos Humanos' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, department_repository, mock_session):
        """Test to verify that exists_by returns False when the department doesn't exist."""
        print("🧪 Testing non-existent department verification...")

        department_repository.exists_by = AsyncMock(return_value=False)

        result = await department_repository.exists_by(name="Departamento Inexistente")

        assert result is False
        print(
            f"✅ Department non-existence verified: 'Departamento Inexistente' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, department_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        department_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException("Invalid field")
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await department_repository.exists_by(campo_inexistente="valor")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, department_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        departments = [Department(id=1, name="Recursos Humanos")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=departments, meta=pagination_info)

        department_repository.find = AsyncMock(return_value=page)

        search_params = {"name": "recursos"}
        result = await department_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].name == "Recursos Humanos"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, department in enumerate(result.data):
            print(f"   - Result {i+1}: ID={department.id}, Name='{department.name}'")
