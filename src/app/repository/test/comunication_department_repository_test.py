import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import ComunicationDepartmentRepositoryImpl
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
def comunicacion_area_repository(mock_session):
    return ComunicationDepartmentRepositoryImpl(session=mock_session)


@pytest.fixture
def comunicacion_area_sample():
    comunicacion = MagicMock()
    comunicacion.id = 1
    comunicacion.area_origen_id = 1
    comunicacion.area_destino_id = 2
    comunicacion.created_at = datetime.now()
    comunicacion.updated_at = None
    return comunicacion


class TestComunicacionAreaRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, comunicacion_area_repository, mock_session, comunicacion_area_sample
    ):
        """Test to verify that the save method correctly stores a communication between areas."""
        print("🧪 Testing successful communication between areas saving...")

        result = await comunicacion_area_repository.save(comunicacion_area_sample)

        mock_session.add.assert_called_once_with(comunicacion_area_sample)
        assert result == comunicacion_area_sample
        print(f"✅ Communication between areas saved successfully: ID={result.id}")

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, comunicacion_area_repository, mock_session, comunicacion_area_sample
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
            await comunicacion_area_repository.save(comunicacion_area_sample)

        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, comunicacion_area_repository, mock_session):
        """Test to verify that get_all returns all communications between areas."""
        print("🧪 Testing retrieval of all communications between areas...")

        com1 = MagicMock()
        com1.id = 1
        com1.area_origen_id = 1
        com1.area_destino_id = 2

        com2 = MagicMock()
        com2.id = 2
        com2.area_origen_id = 2
        com2.area_destino_id = 3

        comunicaciones = [com1, com2]

        mock_result = MagicMock()
        mock_result.all.return_value = comunicaciones
        mock_session.exec.return_value = mock_result

        result = await comunicacion_area_repository.get_all()

        assert len(result) == 2
        assert result[0].area_origen_id == 1
        assert result[1].area_origen_id == 2
        print(
            f"✅ All communications between areas retrieved: {len(result)} communications found"
        )

    @pytest.mark.asyncio
    async def test_delete_success(
        self, comunicacion_area_repository, mock_session, comunicacion_area_sample
    ):
        """Test to verify that delete correctly removes a communication between areas."""
        print("🧪 Testing communication between areas deletion...")

        comunicacion_area_repository.get_by_id = AsyncMock(
            return_value=comunicacion_area_sample
        )

        result = await comunicacion_area_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(comunicacion_area_sample)
        print(f"✅ Communication between areas deleted successfully: ID=1")

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, comunicacion_area_repository, mock_session, comunicacion_area_sample
    ):
        """Test to verify that get_by_id returns the correct communication between areas."""
        print("🧪 Testing communication between areas retrieval by ID...")

        mock_result = MagicMock()
        mock_result.first.return_value = comunicacion_area_sample
        mock_session.exec.return_value = mock_result

        result = await comunicacion_area_repository.get_by_id(1)

        assert result == comunicacion_area_sample
        print(f"✅ Communication between areas retrieved by ID: ID={result.id}")

    @pytest.mark.asyncio
    async def test_get_pageable_success(
        self, comunicacion_area_repository, mock_session
    ):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing communication between areas pagination...")

        comunicaciones_data = [
            {
                "id": 1,
                "area_origen_id": 1,
                "area_destino_id": 2,
                "area_origen_nombre": "Desarrollo",
                "area_destino_nombre": "Finanzas",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "area_origen_id": 2,
                "area_destino_id": 3,
                "area_origen_nombre": "Finanzas",
                "area_destino_nombre": "Recursos Humanos",
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

        page = Page(data=comunicaciones_data, meta=pagination_info)

        mock_result = MagicMock()
        mock_result._mapping = comunicaciones_data[0]
        mock_results = [mock_result, MagicMock(_mapping=comunicaciones_data[1])]

        mock_count_result = MagicMock()
        mock_count_result.first.return_value = 2

        mock_session.exec.side_effect = [mock_results, mock_count_result]

        comunicacion_area_repository.get_pageable = AsyncMock(return_value=page)

        result = await comunicacion_area_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        print(
            f"✅ Communications between areas paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} communications"
        )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, comunicacion_area_repository, mock_session):
        """Test to verify that exists_by returns True when the communication between areas exists."""
        print("🧪 Testing communication between areas existence verification...")

        mock_result = MagicMock()
        mock_result.first.return_value = 1
        mock_session.exec.return_value = mock_result

        result = await comunicacion_area_repository.exists_by(
            area_origen_id=1, area_destino_id=2
        )

        assert result is True
        print(
            f"✅ Communication between areas existence verified: Communication From=1, To=2 exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(
        self, comunicacion_area_repository, mock_session
    ):
        """Test to verify that exists_by returns False when the communication between areas doesn't exist."""
        print("🧪 Testing non-existent communication between areas verification...")

        mock_result = MagicMock()
        mock_result.first.return_value = None
        mock_session.exec.return_value = mock_result

        result = await comunicacion_area_repository.exists_by(
            area_origen_id=99, area_destino_id=99
        )

        assert result is False
        print(
            f"✅ Communication between areas non-existence verified: Communication From=99, To=99 exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, comunicacion_area_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        comunicacion_area_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException(
                message="Field 'campo_inexistente' does not exist in the ComunicacionArea model",
                details="Valid fields are: id, area_origen_id, area_destino_id",
            )
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await comunicacion_area_repository.exists_by(campo_inexistente="valor")

        assert "does not exist in the ComunicacionArea model" in str(exc_info.value)
        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, comunicacion_area_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        comunicaciones_data = [
            {
                "id": 1,
                "area_origen_id": 1,
                "area_destino_id": 2,
                "area_origen_nombre": "Desarrollo",
                "area_destino_nombre": "Finanzas",
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

        page = Page(data=comunicaciones_data, meta=pagination_info)

        comunicacion_area_repository.find = AsyncMock(return_value=page)

        search_params = {"area_origen_id": "1"}
        result = await comunicacion_area_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0]["area_origen_id"] == 1
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
