import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.repository.implementations import CategoriaRepositoryImpl
from src.model.entity import CategoriaDocumento
from src.exception import DatabaseException, InvalidFieldException
from src.schema import Page, Pagination


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def categoria_repository(mock_session):
    return CategoriaRepositoryImpl(session=mock_session)


@pytest.fixture
def categoria_documento_sample():
    return CategoriaDocumento(
        id=1,
        nombre="Documentos Financieros",
        created_at=datetime.now(),
        updated_at=None
    )


class TestCategoriaRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(self, categoria_repository, mock_session, categoria_documento_sample):
        """Test to verify that the save method correctly stores a category."""
        print("🧪 Testing successful category saving...")

        result = await categoria_repository.save(categoria_documento_sample)

        mock_session.add.assert_called_once_with(categoria_documento_sample)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(categoria_documento_sample)
        assert result == categoria_documento_sample
        print(f"✅ Category saved successfully: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_save_integrity_error(self, categoria_repository, mock_session, categoria_documento_sample):
        """Test to verify that save method correctly handles integrity errors."""
        print("🧪 Testing integrity error handling during save...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError("Duplicate entry", None, error_original)

        with pytest.raises(DatabaseException) as exc_info:
            await categoria_repository.save(categoria_documento_sample)

        assert "Data integrity error" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, categoria_repository, mock_session):
        """Test to verify that get_all returns all categories."""
        print("🧪 Testing retrieval of all categories...")

        categorias = [
            CategoriaDocumento(id=1, nombre="Documentos Financieros"),
            CategoriaDocumento(id=2, nombre="Documentos Técnicos")
        ]

        categoria_repository.get_all = AsyncMock(return_value=categorias)

        result = await categoria_repository.get_all()

        assert len(result) == 2
        assert result[0].nombre == "Documentos Financieros"
        assert result[1].nombre == "Documentos Técnicos"
        print(f"✅ All categories retrieved: {len(result)} categories found")
        for i, cat in enumerate(result):
            print(f"   - Category {i+1}: ID={cat.id}, Name='{cat.nombre}'")

    @pytest.mark.asyncio
    async def test_delete_success(self, categoria_repository, mock_session, categoria_documento_sample):
        """Test to verify that delete correctly removes a category."""
        print("🧪 Testing category deletion...")

        categoria_repository.get_by_id = AsyncMock(return_value=categoria_documento_sample)

        result = await categoria_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(categoria_documento_sample)
        mock_session.commit.assert_called_once()
        print(f"✅ Category deleted successfully: ID=1, Name='{categoria_documento_sample.nombre}'")

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, categoria_repository, mock_session, categoria_documento_sample):
        """Test to verify that get_by_id returns the correct category."""
        print("🧪 Testing category retrieval by ID...")

        categoria_repository.get_by_id = AsyncMock(return_value=categoria_documento_sample)

        result = await categoria_repository.get_by_id(1)

        assert result == categoria_documento_sample
        assert result.nombre == "Documentos Financieros"
        print(f"✅ Category retrieved by ID: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, categoria_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing category pagination...")

        categorias = [
            CategoriaDocumento(id=1, nombre="Documentos Financieros"),
            CategoriaDocumento(id=2, nombre="Documentos Técnicos")
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=0,
            previous_page=0
        )

        pagina = Page(
            data=categorias,
            meta=pagination_info
        )

        categoria_repository.get_pageable = AsyncMock(return_value=pagina)

        result = await categoria_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(f"✅ Categories paginated: Page {result.meta.current_page}/{result.meta.total_pages}, " 
              f"showing {len(result.data)} of {result.meta.total} categories")
        for i, cat in enumerate(result.data):
            print(f"   - Category {i+1}: ID={cat.id}, Name='{cat.nombre}'")

    @pytest.mark.asyncio
    async def test_exists_by_success(self, categoria_repository, mock_session):
        """Test to verify that exists_by returns True when the category exists."""
        print("🧪 Testing category existence verification...")

        categoria_repository.exists_by = AsyncMock(return_value=True)

        result = await categoria_repository.exists_by(nombre="Documentos Financieros")

        assert result is True
        print(f"✅ Category existence verified: 'Documentos Financieros' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, categoria_repository, mock_session):
        """Test to verify that exists_by returns False when the category doesn't exist."""
        print("🧪 Testing non-existent category verification...")

        categoria_repository.exists_by = AsyncMock(return_value=False)

        result = await categoria_repository.exists_by(nombre="Categoría Inexistente")

        assert result is False
        print(f"✅ Category non-existence verified: 'Categoría Inexistente' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, categoria_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        categoria_repository.exists_by = AsyncMock(side_effect=InvalidFieldException("Invalid field"))

        with pytest.raises(InvalidFieldException) as exc_info:
            await categoria_repository.exists_by(campo_inexistente="valor")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, categoria_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        categorias = [CategoriaDocumento(id=1, nombre="Documentos Financieros")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=0,
            previous_page=0
        )

        pagina = Page(
            data=categorias,
            meta=pagination_info
        )

        categoria_repository.find = AsyncMock(return_value=pagina)

        search_params = {"nombre": "financieros"}
        result = await categoria_repository.find(page=1, size=10, search_dict=search_params)

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].nombre == "Documentos Financieros"
        assert result.meta.total == 1
        print(f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}")
        for i, cat in enumerate(result.data):
            print(f"   - Result {i+1}: ID={cat.id}, Name='{cat.nombre}'")