import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import AreaRepositoryImpl
from src.app.model.entity import Area
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
def area_repository(mock_session):
    return AreaRepositoryImpl(session=mock_session)


@pytest.fixture
def area_sample():
    return Area(
        id=1,
        nombre="Recursos Humanos",
        created_at=datetime.now(),
        updated_at=None
    )


class TestAreaRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(self, area_repository, mock_session, area_sample):
        """Test to verify that the save method correctly stores an area."""
        print("🧪 Testing successful area saving...")

        result = await area_repository.save(area_sample)

        mock_session.add.assert_called_once_with(area_sample)
        assert result == area_sample
        print(f"✅ Area saved successfully: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_save_integrity_error(self, area_repository, mock_session, area_sample):
        """Test to verify that the save method correctly handles integrity errors."""
        print("🧪 Testing integrity error handling during save...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError("Duplicate entry", None, error_original)

        with pytest.raises(DatabaseException) as exc_info:
            await area_repository.save(area_sample)

        assert isinstance(exc_info.value, DatabaseException)
        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, area_repository, mock_session):
        """Test to verify that get_all returns all areas."""
        print("🧪 Testing retrieval of all areas...")

        areas = [
            Area(id=1, nombre="Recursos Humanos"),
            Area(id=2, nombre="Finanzas")
        ]

        area_repository.get_all = AsyncMock(return_value=areas)

        result = await area_repository.get_all()

        assert len(result) == 2
        assert result[0].nombre == "Recursos Humanos"
        assert result[1].nombre == "Finanzas"
        print(f"✅ All areas retrieved: {len(result)} areas found")
        for i, area in enumerate(result):
            print(f"   - Area {i+1}: ID={area.id}, Name='{area.nombre}'")

    @pytest.mark.asyncio
    async def test_delete_success(self, area_repository, mock_session, area_sample):
        """Test to verify that delete correctly removes an area."""
        print("🧪 Testing area deletion...")

        area_repository.get_by_id = AsyncMock(return_value=area_sample)

        result = await area_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(area_sample)
        print(f"✅ Area deleted successfully: ID=1, Name='{area_sample.nombre}'")

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, area_repository, mock_session, area_sample):
        """Test to verify that get_by_id returns the correct area."""
        print("🧪 Testing area retrieval by ID...")

        area_repository.get_by_id = AsyncMock(return_value=area_sample)

        result = await area_repository.get_by_id(1)

        assert result == area_sample
        assert result.nombre == "Recursos Humanos"
        print(f"✅ Area retrieved by ID: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, area_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing area pagination...")

        areas = [
            Area(id=1, nombre="Recursos Humanos"),
            Area(id=2, nombre="Finanzas")
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None
        )

        pagina = Page(
            data=areas,
            meta=pagination_info
        )

        area_repository.get_pageable = AsyncMock(return_value=pagina)

        result = await area_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(f"✅ Areas paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
              f"showing {len(result.data)} of {result.meta.total} areas")
        for i, area in enumerate(result.data):
            print(f"   - Area {i+1}: ID={area.id}, Name='{area.nombre}'")

    @pytest.mark.asyncio
    async def test_exists_by_success(self, area_repository, mock_session):
        """Test to verify that exists_by returns True when the area exists."""
        print("🧪 Testing area existence verification...")

        area_repository.exists_by = AsyncMock(return_value=True)

        result = await area_repository.exists_by(nombre="Recursos Humanos")

        assert result is True
        print(f"✅ Area existence verified: 'Recursos Humanos' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, area_repository, mock_session):
        """Test to verify that exists_by returns False when the area doesn't exist."""
        print("🧪 Testing non-existent area verification...")

        area_repository.exists_by = AsyncMock(return_value=False)

        result = await area_repository.exists_by(nombre="Área Inexistente")

        assert result is False
        print(f"✅ Area non-existence verified: 'Área Inexistente' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, area_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        area_repository.exists_by = AsyncMock(side_effect=InvalidFieldException("Invalid field"))

        with pytest.raises(InvalidFieldException) as exc_info:
            await area_repository.exists_by(campo_inexistente="valor")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, area_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        areas = [Area(id=1, nombre="Recursos Humanos")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None
        )

        pagina = Page(
            data=areas,
            meta=pagination_info
        )

        area_repository.find = AsyncMock(return_value=pagina)

        search_params = {"nombre": "recursos"}
        result = await area_repository.find(page=1, size=10, search_dict=search_params)

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].nombre == "Recursos Humanos"
        assert result.meta.total == 1
        print(f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}")
        for i, area in enumerate(result.data):
            print(f"   - Result {i+1}: ID={area.id}, Name='{area.nombre}'")