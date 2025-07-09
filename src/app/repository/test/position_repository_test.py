import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import PositionRepositoryImpl
from src.app.model.entity import Position
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
def position_repository(mock_session):
    return PositionRepositoryImpl(session=mock_session)


@pytest.fixture
def position_sample():
    return Position(
        id=1, name="Project Manager", created_at=datetime.now(), updated_at=None
    )


class TestPositionRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, position_repository, mock_session, position_sample
    ):
        """Test to verify that the save method correctly stores a position."""
        print("🧪 Testing successful position saving...")

        result = await position_repository.save(position_sample)

        mock_session.add.assert_called_once_with(position_sample)
        assert result == position_sample
        print(f"✅ Position saved successfully: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, position_repository, mock_session, position_sample
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
            await position_repository.save(position_sample)

        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, position_repository, mock_session):
        """Test to verify that get_all returns all positions."""
        print("🧪 Testing retrieval of all positions...")

        positions = [
            Position(id=1, name="Project Manager"),
            Position(id=2, name="Developer"),
        ]

        position_repository.get_all = AsyncMock(return_value=positions)

        result = await position_repository.get_all()

        assert len(result) == 2
        assert result[0].name == "Project Manager"
        assert result[1].name == "Developer"
        print(f"✅ All positions retrieved: {len(result)} positions found")
        for i, pos in enumerate(result):
            print(f"   - Position {i+1}: ID={pos.id}, Name='{pos.name}'")

    @pytest.mark.asyncio
    async def test_delete_success(
        self, position_repository, mock_session, position_sample
    ):
        """Test to verify that delete correctly removes a position."""
        print("🧪 Testing position deletion...")

        position_repository.get_by_id = AsyncMock(return_value=position_sample)

        result = await position_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(position_sample)
        mock_session.commit.assert_called_once()
        print(f"✅ Position deleted successfully: ID=1, Name='{position_sample.name}'")

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, position_repository, mock_session, position_sample
    ):
        """Test to verify that get_by_id returns the correct position."""
        print("🧪 Testing position retrieval by ID...")

        position_repository.get_by_id = AsyncMock(return_value=position_sample)

        result = await position_repository.get_by_id(1)

        assert result == position_sample
        assert result.name == "Project Manager"
        print(f"✅ Position retrieved by ID: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, position_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing position pagination...")

        positions = [
            Position(id=1, name="Project Manager"),
            Position(id=2, name="Developer"),
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page_obj = Page(data=positions, meta=pagination_info)

        position_repository.get_pageable = AsyncMock(return_value=page_obj)

        result = await position_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Positions paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} positions"
        )
        for i, pos in enumerate(result.data):
            print(f"   - Position {i+1}: ID={pos.id}, Name='{pos.name}'")

    @pytest.mark.asyncio
    async def test_exists_by_success(self, position_repository, mock_session):
        """Test to verify that exists_by returns True when the position exists."""
        print("🧪 Testing position existence verification...")

        position_repository.exists_by = AsyncMock(return_value=True)

        result = await position_repository.exists_by(name="Project Manager")

        assert result is True
        print(f"✅ Position existence verified: 'Project Manager' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, position_repository, mock_session):
        """Test to verify that exists_by returns False when the position doesn't exist."""
        print("🧪 Testing non-existent position verification...")

        position_repository.exists_by = AsyncMock(return_value=False)

        result = await position_repository.exists_by(name="Non-existent Position")

        assert result is False
        print(
            f"✅ Position non-existence verified: 'Non-existent Position' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, position_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        position_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException("Invalid field")
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await position_repository.exists_by(non_existent_field="value")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, position_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        positions = [Position(id=1, name="Project Manager")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page_obj = Page(data=positions, meta=pagination_info)

        position_repository.find = AsyncMock(return_value=page_obj)

        search_params = {"name": "manager"}
        result = await position_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].name == "Project Manager"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, pos in enumerate(result.data):
            print(f"   - Result {i+1}: ID={pos.id}, Name='{pos.name}'")
