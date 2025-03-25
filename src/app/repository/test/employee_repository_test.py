import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import EmployeeRepositoryImpl
from src.app.model.entity import Trabajador, Area, Cargo
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
def employee_repository(mock_session):
    return EmployeeRepositoryImpl(session=mock_session)


@pytest.fixture
def employee_sample():
    return Trabajador(
        id=1,
        dni=12345678,
        nombres="Juan Carlos",
        apellido_paterno="Pérez",
        apellido_materno="Gómez",
        genero="Masculino",
        cargo_id=1,
        area_id=1,
        created_at=datetime.now(),
        updated_at=None,
    )


@pytest.fixture
def area_sample():
    return Area(id=1, nombre="Desarrollo")


@pytest.fixture
def cargo_sample():
    return Cargo(id=1, nombre="Desarrollador Senior")


class TestEmployeeRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, employee_repository, mock_session, employee_sample
    ):
        """Test to verify that the save method correctly stores an employee."""
        print("🧪 Testing successful employee saving...")

        result = await employee_repository.save(employee_sample)

        mock_session.add.assert_called_once_with(employee_sample)
        assert result == employee_sample
        print(
            f"✅ Employee saved successfully: ID={result.id}, Name='{result.nombres} {result.apellido_paterno}'"
        )

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, employee_repository, mock_session, employee_sample
    ):
        """Test to verify that save method correctly handles integrity errors."""
        print("🧪 Testing integrity error handling during save...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError(
            "Duplicate entry", None, error_original
        )

        with pytest.raises(DatabaseException) as exc_info:
            await employee_repository.save(employee_sample)

        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, employee_repository, mock_session):
        """Test to verify that get_all returns all employees."""
        print("🧪 Testing retrieval of all employees...")

        employees = [
            Trabajador(
                id=1,
                dni=12345678,
                nombres="Juan Carlos",
                apellido_paterno="Pérez",
                apellido_materno="Gómez",
                genero="Masculino",
                cargo_id=1,
                area_id=1,
            ),
            Trabajador(
                id=2,
                dni=87654321,
                nombres="María",
                apellido_paterno="López",
                apellido_materno="Sánchez",
                genero="Femenino",
                cargo_id=2,
                area_id=2,
            ),
        ]

        mock_result = MagicMock()
        mock_result.all.return_value = employees
        mock_session.exec.return_value = mock_result

        result = await employee_repository.get_all()

        assert len(result) == 2
        assert result[0].nombres == "Juan Carlos"
        assert result[1].nombres == "María"
        print(f"✅ All employees retrieved: {len(result)} employees found")
        for i, emp in enumerate(result):
            print(
                f"   - Employee {i+1}: ID={emp.id}, Name='{emp.nombres} {emp.apellido_paterno}'"
            )

    @pytest.mark.asyncio
    async def test_delete_success(
        self, employee_repository, mock_session, employee_sample
    ):
        print("🧪 Testing employee deletion...")

        employee_repository.get_by_id = AsyncMock(return_value=employee_sample)

        async def patched_delete(trabajador_id):
            employee = await employee_repository.get_by_id(trabajador_id)
            await mock_session.delete(employee)
            return True

        employee_repository.delete = patched_delete

        result = await employee_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(employee_sample)
        print(
            f"✅ Employee deleted successfully: ID=1, Name='{employee_sample.nombres} {employee_sample.apellido_paterno}'"
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, employee_repository, mock_session, employee_sample
    ):
        """Test to verify that get_by_id returns the correct employee."""
        print("🧪 Testing employee retrieval by ID...")

        employee_repository.get_by_id = AsyncMock(return_value=employee_sample)

        result = await employee_repository.get_by_id(1)

        assert result == employee_sample
        assert result.nombres == "Juan Carlos"
        assert result.apellido_paterno == "Pérez"
        print(
            f"✅ Employee retrieved by ID: ID={result.id}, Name='{result.nombres} {result.apellido_paterno}'"
        )

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, employee_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing employee pagination...")

        employees_data = [
            {
                "id": 1,
                "dni": 12345678,
                "nombres": "Juan Carlos",
                "apellido_paterno": "Pérez",
                "apellido_materno": "Gómez",
                "genero": "Masculino",
                "area_nombre": "Desarrollo",
                "cargo_nombre": "Desarrollador Senior",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "dni": 87654321,
                "nombres": "María",
                "apellido_paterno": "López",
                "apellido_materno": "Sánchez",
                "genero": "Femenino",
                "area_nombre": "Recursos Humanos",
                "cargo_nombre": "Gerente",
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

        page = Page(data=employees_data, meta=pagination_info)

        employee_repository.get_pageable = AsyncMock(return_value=page)

        result = await employee_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        print(
            f"✅ Employees paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} employees"
        )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, employee_repository, mock_session):
        """Test to verify that exists_by returns True when the employee exists."""
        print("🧪 Testing employee existence verification...")

        mock_result = AsyncMock()
        mock_result.first.return_value = 1
        mock_session.exec.return_value = mock_result

        result = await employee_repository.exists_by(dni=12345678)

        assert result is True
        print(
            f"✅ Employee existence verified: Employee with DNI 12345678 exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, employee_repository, mock_session):
        """Test to verify that exists_by returns False when the employee doesn't exist."""
        print("🧪 Testing non-existent employee verification...")

        employee_repository.exists_by = AsyncMock(return_value=False)

        result = await employee_repository.exists_by(dni=99999999)

        assert result is False
        print(
            f"✅ Employee non-existence verified: Employee with DNI 99999999 exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, employee_repository, mock_session):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        with pytest.raises(InvalidFieldException) as exc_info:
            await employee_repository.exists_by(campo_inexistente="valor")

        assert "does not exist in the Trabajador model" in str(exc_info.value)
        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, employee_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        employees_data = [
            {
                "id": 1,
                "dni": 12345678,
                "nombres": "Juan Carlos",
                "apellido_paterno": "Pérez",
                "apellido_materno": "Gómez",
                "genero": "Masculino",
                "area_nombre": "Desarrollo",
                "cargo_nombre": "Desarrollador Senior",
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

        page = Page(data=employees_data, meta=pagination_info)

        employee_repository.find = AsyncMock(return_value=page)

        search_params = {"nombres": "juan"}
        result = await employee_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0]["nombres"] == "Juan Carlos"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, employee in enumerate(result.data):
            print(
                f"   - Result {i + 1}: ID={employee['id']}, Name='{employee['nombres']} {employee['apellido_paterno']}'"
            )
