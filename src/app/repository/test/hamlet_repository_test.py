import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import HamletRepositoryImpl
from src.app.model.entity import Hamlet, Settlement
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
def hamlet_repository(mock_session):
    return HamletRepositoryImpl(session=mock_session)


@pytest.fixture
def hamlet_sample():
    return Hamlet(
        id=1,
        name="El Paraíso",
        settlement_id=1,
        created_at=datetime.now(),
        updated_at=None,
    )


@pytest.fixture
def settlement_sample():
    return Settlement(id=1, name="San Juan")


class TestHamletRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(self, hamlet_repository, mock_session, hamlet_sample):
        """Test to verify that the save method correctly stores a hamlet."""
        print("🧪 Testing successful hamlet saving...")

        result = await hamlet_repository.save(hamlet_sample)

        mock_session.add.assert_called_once_with(hamlet_sample)
        assert result == hamlet_sample
        print(f"✅ Hamlet saved successfully: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, hamlet_repository, mock_session, hamlet_sample
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
            await hamlet_repository.save(hamlet_sample)

        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, hamlet_repository, mock_session):
        """Test to verify that get_all returns all hamlets."""
        print("🧪 Testing retrieval of all hamlets...")

        hamlets = [
            Hamlet(
                id=1,
                name="El Paraíso",
                settlement_id=1,
            ),
            Hamlet(
                id=2,
                name="Las Flores",
                settlement_id=1,
            ),
        ]

        mock_result = MagicMock()
        mock_result.all.return_value = hamlets
        mock_session.exec.return_value = mock_result

        result = await hamlet_repository.get_all()

        assert len(result) == 2
        assert result[0].name == "El Paraíso"
        assert result[1].name == "Las Flores"
        print(f"✅ All hamlets retrieved: {len(result)} hamlets found")
        for i, hamlet in enumerate(result):
            print(f"   - Hamlet {i+1}: ID={hamlet.id}, Name='{hamlet.name}'")

    @pytest.mark.asyncio
    async def test_delete_success(self, hamlet_repository, mock_session, hamlet_sample):
        """Test to verify that delete successfully removes a hamlet."""
        print("🧪 Testing hamlet deletion...")

        hamlet_repository.get_by_id = AsyncMock(return_value=hamlet_sample)

        async def patched_delete(hamlet_id):
            hamlet = await hamlet_repository.get_by_id(hamlet_id)
            await mock_session.delete(hamlet)
            await mock_session.commit()
            return True

        hamlet_repository.delete = patched_delete

        result = await hamlet_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(hamlet_sample)
        print(f"✅ Hamlet deleted successfully: ID=1, Name='{hamlet_sample.name}'")

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, hamlet_repository, mock_session, hamlet_sample
    ):
        """Test to verify that get_by_id returns the correct hamlet."""
        print("🧪 Testing hamlet retrieval by ID...")

        mock_result = MagicMock()
        mock_result.first.return_value = hamlet_sample
        mock_session.exec.return_value = mock_result

        hamlet_repository.get_by_id = AsyncMock(return_value=hamlet_sample)

        result = await hamlet_repository.get_by_id(1)

        assert result == hamlet_sample
        assert result.name == "El Paraíso"
        print(f"✅ Hamlet retrieved by ID: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, hamlet_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing hamlet pagination...")

        hamlets_data = [
            {
                "id": 1,
                "name": "El Paraíso",
                "settlement_id": 1,
                "settlement_name": "San Juan",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "name": "Las Flores",
                "settlement_id": 1,
                "settlement_name": "San Juan",
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

        page = Page(data=hamlets_data, meta=pagination_info)

        hamlet_repository.get_pageable = AsyncMock(return_value=page)

        result = await hamlet_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        print(
            f"✅ Hamlets paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} hamlets"
        )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, hamlet_repository, mock_session):
        """Test to verify that exists_by returns True when the hamlet exists."""
        print("🧪 Testing hamlet existence verification...")

        mock_result = AsyncMock()
        mock_result.first.return_value = 1
        mock_session.exec.return_value = mock_result

        result = await hamlet_repository.exists_by(name="El Paraíso")

        assert result is True
        print(
            f"✅ Hamlet existence verified: Hamlet with name 'El Paraíso' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, hamlet_repository, mock_session):
        """Test to verify that exists_by returns False when the hamlet doesn't exist."""
        print("🧪 Testing non-existent hamlet verification...")

        hamlet_repository.exists_by = AsyncMock(return_value=False)

        result = await hamlet_repository.exists_by(name="Non-existent Hamlet")

        assert result is False
        print(
            f"✅ Hamlet non-existence verified: Hamlet with name 'Non-existent Hamlet' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, hamlet_repository, mock_session):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        with pytest.raises(InvalidFieldException) as exc_info:
            await hamlet_repository.exists_by(non_existent_field="value")

        assert "does not exist in the Hamlet model" in str(exc_info.value)
        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, hamlet_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        hamlets_data = [
            {
                "id": 1,
                "name": "El Paraíso",
                "settlement_id": 1,
                "settlement_name": "San Juan",
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

        page = Page(data=hamlets_data, meta=pagination_info)

        hamlet_repository.find = AsyncMock(return_value=page)

        search_params = {"name": "paraíso"}
        result = await hamlet_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0]["name"] == "El Paraíso"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, hamlet in enumerate(result.data):
            print(f"   - Result {i + 1}: ID={hamlet['id']}, Name='{hamlet['name']}'")
