import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import SubmitterRepositoryImpl
from src.app.model.entity import Remitente
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
def submitter_repository(mock_session):
    return SubmitterRepositoryImpl(session=mock_session)


@pytest.fixture
def submitter_sample():
    return Remitente(
        id=1,
        nombres="Remitente Test",
        created_at=datetime.now(),
        updated_at=None,
    )


class TestSubmitterRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, submitter_repository, mock_session, submitter_sample
    ):
        """Test to verify that the save method correctly stores a submitter."""
        print("🧪 Probando guardado exitoso de remitente...")

        result = await submitter_repository.save(submitter_sample)

        mock_session.add.assert_called_once_with(submitter_sample)
        assert result == submitter_sample
        print(
            f"✅ Remitente guardado exitosamente: ID={result.id}, Nombre='{result.nombres}'"
        )

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, submitter_repository, mock_session, submitter_sample
    ):
        """Test to verify that the save method correctly handles integrity errors."""
        print("🧪 Probando manejo de error de integridad durante guardado...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Entrada duplicada"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError(
            "Entrada duplicada", None, error_original
        )

        with pytest.raises(DatabaseException) as exc_info:
            await submitter_repository.save(submitter_sample)

        assert isinstance(exc_info.value, DatabaseException)
        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Error de integridad manejado correctamente: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, submitter_repository, mock_session):
        """Test to verify that get_all returns all submitters."""
        print("🧪 Probando obtención de todos los remitentes...")

        submitters = [
            Remitente(id=1, nombres="Remitente 1"),
            Remitente(id=2, nombres="Remitente 2"),
        ]

        submitter_repository.get_all = AsyncMock(return_value=submitters)

        result = await submitter_repository.get_all()

        assert len(result) == 2
        assert result[0].nombres == "Remitente 1"
        assert result[1].nombres == "Remitente 2"
        print(
            f"✅ Todos los remitentes obtenidos: {len(result)} remitentes encontrados"
        )
        for i, submitter in enumerate(result):
            print(
                f"   - Remitente {i+1}: ID={submitter.id}, Nombre='{submitter.nombres}'"
            )

    @pytest.mark.asyncio
    async def test_delete_success(
        self, submitter_repository, mock_session, submitter_sample
    ):
        """Test to verify that delete correctly removes a submitter."""
        print("🧪 Probando eliminación de remitente...")

        submitter_repository.get_by_id = AsyncMock(return_value=submitter_sample)

        result = await submitter_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(submitter_sample)
        print(
            f"✅ Remitente eliminado exitosamente: ID=1, Nombre='{submitter_sample.nombres}'"
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, submitter_repository, mock_session, submitter_sample
    ):
        """Test to verify that get_by_id returns the correct submitter."""
        print("🧪 Probando obtención de remitente por ID...")

        submitter_repository.get_by_id = AsyncMock(return_value=submitter_sample)

        result = await submitter_repository.get_by_id(1)

        assert result == submitter_sample
        assert result.nombres == "Remitente Test"
        print(
            f"✅ Remitente obtenido por ID: ID={result.id}, Nombre='{result.nombres}'"
        )

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, submitter_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Probando paginación de remitentes...")

        submitters = [
            Remitente(id=1, nombres="Remitente 1"),
            Remitente(id=2, nombres="Remitente 2"),
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        pagina = Page(data=submitters, meta=pagination_info)

        submitter_repository.get_pageable = AsyncMock(return_value=pagina)

        result = await submitter_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Remitentes paginados: Página {result.meta.current_page}/{result.meta.total_pages}, "
            f"mostrando {len(result.data)} de {result.meta.total} remitentes"
        )
        for i, submitter in enumerate(result.data):
            print(
                f"   - Remitente {i+1}: ID={submitter.id}, Nombre='{submitter.nombres}'"
            )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, submitter_repository, mock_session):
        """Test to verify that exists_by returns True when the submitter exists."""
        print("🧪 Probando verificación de existencia de remitente...")

        submitter_repository.exists_by = AsyncMock(return_value=True)

        result = await submitter_repository.exists_by(nombres="Remitente Test")

        assert result is True
        print(
            f"✅ Existencia de remitente verificada: 'Remitente Test' existe = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, submitter_repository, mock_session):
        """Test to verify that exists_by returns False when the submitter does not exist."""
        print("🧪 Probando verificación de remitente inexistente...")

        submitter_repository.exists_by = AsyncMock(return_value=False)

        result = await submitter_repository.exists_by(nombres="Remitente Inexistente")

        assert result is False
        print(
            f"✅ Verificación de inexistencia de remitente: 'Remitente Inexistente' existe = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, submitter_repository):
        """Test to verify that exists_by handles invalid field correctly."""
        print("🧪 Probando manejo de campo inválido...")

        submitter_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException("Campo inválido")
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await submitter_repository.exists_by(campo_inexistente="valor")

        print(f"✅ Campo inválido manejado correctamente: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, submitter_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Probando búsqueda con filtros...")

        submitters = [Remitente(id=1, nombres="Empresa Constructora")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        pagina = Page(data=submitters, meta=pagination_info)

        submitter_repository.find = AsyncMock(return_value=pagina)

        search_params = {"nombres": "Empresa"}
        result = await submitter_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].nombres == "Empresa Constructora"
        assert result.meta.total == 1
        print(
            f"✅ Búsqueda con filtros exitosa: Se encontraron {result.meta.total} resultados para criterios {search_params}"
        )
        for i, submitter in enumerate(result.data):
            print(
                f"   - Resultado {i+1}: ID={submitter.id}, Nombre='{submitter.nombres}'"
            )

    @pytest.mark.asyncio
    async def test_find_no_results(self, submitter_repository, mock_session):
        """Test to verify that find returns no results when there are none."""
        print("🧪 Probando búsqueda con filtros (sin resultados)...")

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        pagina = Page(data=[], meta=pagination_info)

        submitter_repository.find = AsyncMock(return_value=pagina)

        search_params = {"nombres": "inexistente"}
        result = await submitter_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 0
        assert result.meta.total == 0
        print(
            f"✅ Búsqueda con filtros (sin resultados) exitosa: Se encontraron {result.meta.total} resultados para criterios {search_params}"
        )
