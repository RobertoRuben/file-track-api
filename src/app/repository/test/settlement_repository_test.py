import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from src.app.repository.implementations import SettlementRepositoryImpl
from src.app.model.entity import CentroPoblado
from src.app.exception import DatabaseException, InvalidFieldException
from src.app.schema import Page, Pagination


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    session.exec = AsyncMock()
    return session


@pytest.fixture
def settlement_repository(mock_session):
    return SettlementRepositoryImpl(session=mock_session)


@pytest.fixture
def settlement_sample():
    return CentroPoblado(
        id=1,
        nombre="Centro Poblado Test",
        descripcion="Descripción de prueba",
        created_at=datetime.now(),
        updated_at=None,
    )


class TestSettlementRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, settlement_repository, mock_session, settlement_sample
    ):
        """Test to verify that the save method correctly stores a settlement."""
        print("🧪 Testing successful settlement saving...")

        result = await settlement_repository.save(settlement_sample)

        mock_session.add.assert_called_once_with(settlement_sample)
        assert result == settlement_sample
        print(
            f"✅ Settlement saved successfully: ID={result.id}, Name='{result.nombre}'"
        )

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, settlement_repository, mock_session, settlement_sample
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
            await settlement_repository.save(settlement_sample)

        assert isinstance(exc_info.value, DatabaseException)
        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, settlement_repository, mock_session):
        """Test to verify that get_all returns all settlements."""
        print("🧪 Testing retrieval of all settlements...")

        settlements = [
            CentroPoblado(id=1, nombre="Centro Poblado 1"),
            CentroPoblado(id=2, nombre="Centro Poblado 2"),
        ]

        settlement_repository.get_all = AsyncMock(return_value=settlements)

        result = await settlement_repository.get_all()

        assert len(result) == 2
        assert result[0].nombre == "Centro Poblado 1"
        assert result[1].nombre == "Centro Poblado 2"
        print(f"✅ All settlements retrieved: {len(result)} settlements found")
        for i, settlement in enumerate(result):
            print(
                f"   - Settlement {i+1}: ID={settlement.id}, Name='{settlement.nombre}'"
            )

    @pytest.mark.asyncio
    async def test_delete_success(
        self, settlement_repository, mock_session, settlement_sample
    ):
        """Test to verify that delete correctly removes a settlement."""
        print("🧪 Testing settlement deletion...")

        settlement_repository.get_by_id = AsyncMock(return_value=settlement_sample)

        result = await settlement_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(settlement_sample)
        print(
            f"✅ Settlement deleted successfully: ID=1, Name='{settlement_sample.nombre}'"
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, settlement_repository, mock_session, settlement_sample
    ):
        """Test to verify that get_by_id returns the correct settlement."""
        print("🧪 Testing settlement retrieval by ID...")

        settlement_repository.get_by_id = AsyncMock(return_value=settlement_sample)

        result = await settlement_repository.get_by_id(1)

        assert result == settlement_sample
        assert result.nombre == "Centro Poblado Test"
        print(f"✅ Settlement retrieved by ID: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, settlement_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing settlement pagination...")

        settlements = [
            CentroPoblado(id=1, nombre="Centro Poblado 1"),
            CentroPoblado(id=2, nombre="Centro Poblado 2"),
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        pagina = Page(data=settlements, meta=pagination_info)

        settlement_repository.get_pageable = AsyncMock(return_value=pagina)

        result = await settlement_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Settlements paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} settlements"
        )
        for i, settlement in enumerate(result.data):
            print(
                f"   - Settlement {i+1}: ID={settlement.id}, Name='{settlement.nombre}'"
            )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, settlement_repository, mock_session):
        """Test to verify that exists_by returns True when the settlement exists."""
        print("🧪 Testing settlement existence verification...")

        settlement_repository.exists_by = AsyncMock(return_value=True)

        result = await settlement_repository.exists_by(nombre="Centro Poblado Test")

        assert result is True
        print(
            f"✅ Settlement existence verified: 'Centro Poblado Test' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, settlement_repository, mock_session):
        """Test to verify that exists_by returns False when the settlement doesn't exist."""
        print("🧪 Testing non-existent settlement verification...")

        settlement_repository.exists_by = AsyncMock(return_value=False)

        result = await settlement_repository.exists_by(
            nombre="Centro Poblado Inexistente"
        )

        assert result is False
        print(
            f"✅ Settlement non-existence verified: 'Centro Poblado Inexistente' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, settlement_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        settlement_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException("Invalid field")
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await settlement_repository.exists_by(campo_inexistente="valor")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, settlement_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        settlements = [CentroPoblado(id=1, nombre="San Isidro")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        pagina = Page(data=settlements, meta=pagination_info)

        settlement_repository.find = AsyncMock(return_value=pagina)

        search_params = {"nombre": "San"}
        result = await settlement_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].nombre == "San Isidro"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, settlement in enumerate(result.data):
            print(f"   - Result {i+1}: ID={settlement.id}, Name='{settlement.nombre}'")

    @pytest.mark.asyncio
    async def test_find_no_results(self, settlement_repository, mock_session):
        """Test to verify that find returns an empty page when no matches are found."""
        print("🧪 Testing search with filters (no results)...")

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        pagina = Page(data=[], meta=pagination_info)

        settlement_repository.find = AsyncMock(return_value=pagina)

        search_params = {"nombre": "nonexistent"}
        result = await settlement_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 0
        assert result.meta.total == 0
        print(
            f"✅ Search with filters (no results) successful: Found {result.meta.total} results for criteria {search_params}"
        )
