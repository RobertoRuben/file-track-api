import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import DocumentCategoryRepositoryImpl
from src.app.model.entity import DocumentCategory
from src.app.exception import DatabaseException, InvalidFieldException
from src.app.schema import Page, Pagination


@pytest.fixture
def mock_session():
    session = AsyncMock()
    return session


@pytest.fixture
def document_category_repository(mock_session):
    return DocumentCategoryRepositoryImpl(session=mock_session)


@pytest.fixture
def document_category_sample():
    return DocumentCategory(
        id=1,
        name="Financial Documents",
        created_at=datetime.now(),
        updated_at=None,
    )


class TestDocumentCategoryRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
            self, document_category_repository, mock_session, document_category_sample
    ):
        """Test to verify that the save method correctly stores a category."""
        print("🧪 Testing successful category saving...")

        result = await document_category_repository.save(document_category_sample)

        mock_session.add.assert_called_once_with(document_category_sample)
        assert result == document_category_sample
        print(f"✅ Category saved successfully: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_get_all_success(self, document_category_repository, mock_session):
        """Test to verify that get_all returns all categories."""
        print("🧪 Testing retrieval of all categories...")

        categories = [
            DocumentCategory(id=1, name="Financial Documents"),
            DocumentCategory(id=2, name="Technical Documents"),
        ]

        # Corregimos el mock para que devuelva un objeto con método all()
        mock_result = MagicMock()
        mock_result.all.return_value = categories

        # Hacemos que exec() devuelva el mock_result directamente (no un coroutine)
        mock_session.exec.return_value = mock_result

        result = await document_category_repository.get_all()

        assert len(result) == 2
        assert result[0].name == "Financial Documents"
        assert result[1].name == "Technical Documents"
        print(f"✅ All categories retrieved: {len(result)} categories found")
        for i, cat in enumerate(result):
            print(f"   - Category {i+1}: ID={cat.id}, Name='{cat.name}'")

    @pytest.mark.asyncio
    async def test_delete_success(
            self, document_category_repository, mock_session, document_category_sample
    ):
        """Test to verify that delete correctly removes a category."""
        print("🧪 Testing category deletion...")

        # Usamos un método normal para hacer el mock asíncrono
        async def mock_get_by_id(_):
            return document_category_sample

        document_category_repository.get_by_id = mock_get_by_id

        result = await document_category_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(document_category_sample)
        print(
            f"✅ Category deleted successfully: ID=1, Name='{document_category_sample.name}'"
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
            self, document_category_repository, mock_session, document_category_sample
    ):
        """Test to verify that get_by_id returns the correct category."""
        print("🧪 Testing category retrieval by ID...")

        # Usamos MagicMock en lugar de AsyncMock para el resultado
        mock_result = MagicMock()
        mock_result.first.return_value = document_category_sample
        mock_session.exec.return_value = mock_result

        result = await document_category_repository.get_by_id(1)

        assert result == document_category_sample
        assert result.name == "Financial Documents"
        print(f"✅ Category retrieved by ID: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(
            self, document_category_repository, mock_session
    ):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing category pagination...")

        categories = [
            DocumentCategory(id=1, name="Financial Documents"),
            DocumentCategory(id=2, name="Technical Documents"),
        ]

        # Mock para la consulta de datos - usamos MagicMock
        mock_result = MagicMock()
        mock_result.all.return_value = categories

        # Mock para el conteo - usamos MagicMock
        mock_count_result = MagicMock()
        mock_count_result.first.return_value = 2

        # Configuramos los valores de retorno secuenciales
        mock_session.exec.side_effect = [mock_result, mock_count_result]

        result = await document_category_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Categories paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} categories"
        )
        for i, cat in enumerate(result.data):
            print(f"   - Category {i+1}: ID={cat.id}, Name='{cat.name}'")

    @pytest.mark.asyncio
    async def test_exists_by_success(self, document_category_repository, mock_session):
        """Test to verify that exists_by returns True when the category exists."""
        print("🧪 Testing category existence verification...")

        # Usamos MagicMock en lugar de AsyncMock
        mock_result = MagicMock()
        mock_result.first.return_value = 1  # ID encontrado
        mock_session.exec.return_value = mock_result

        result = await document_category_repository.exists_by(
            name="Financial Documents"
        )

        assert result is True
        print(
            f"✅ Category existence verified: 'Financial Documents' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(
            self, document_category_repository, mock_session
    ):
        """Test to verify that exists_by returns False when the category doesn't exist."""
        print("🧪 Testing non-existent category verification...")

        # Usamos MagicMock en lugar de AsyncMock
        mock_result = MagicMock()
        mock_result.first.return_value = None  # No se encontró ID
        mock_session.exec.return_value = mock_result

        result = await document_category_repository.exists_by(
            name="Non-existent Category"
        )

        assert result is False
        print(
            f"✅ Category non-existence verified: 'Non-existent Category' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, document_category_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        with pytest.raises(InvalidFieldException) as exc_info:
            await document_category_repository.exists_by(invalid_field="value")

        assert "does not exist in the DocumentCategory model" in str(exc_info.value)
        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, document_category_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        categories = [DocumentCategory(id=1, name="Financial Documents")]

        # Mock para la consulta de datos - usamos MagicMock
        mock_result = MagicMock()
        mock_result.all.return_value = categories

        # Mock para el conteo - usamos MagicMock
        mock_count_result = MagicMock()
        mock_count_result.first.return_value = 1

        # Configuramos los valores de retorno secuenciales
        mock_session.exec.side_effect = [mock_result, mock_count_result]

        search_params = {"name": "financial"}
        result = await document_category_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].name == "Financial Documents"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, cat in enumerate(result.data):
            print(f"   - Result {i+1}: ID={cat.id}, Name='{cat.name}'")