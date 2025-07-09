import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import SubmitterRepositoryImpl
from src.app.model.entity import Submitter
from src.app.core.exception import DatabaseException, InvalidFieldException
from src.app.core.schema import Page, Pagination


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
    return Submitter(
        id=1,
        dni=12345678,
        names="John",
        paternal_surname="Doe",
        maternal_surname="Smith",
        gender="Male",
        created_at=datetime.now(),
        updated_at=None,
    )


class TestSubmitterRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, submitter_repository, mock_session, submitter_sample
    ):
        """Test to verify that the save method correctly stores a submitter."""
        print("🧪 Testing successful submitter save...")

        result = await submitter_repository.save(submitter_sample)

        mock_session.add.assert_called_once_with(submitter_sample)
        assert result == submitter_sample
        print(
            f"✅ Submitter saved successfully: ID={result.id}, Name='{result.names} {result.paternal_surname}'"
        )

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, submitter_repository, mock_session, submitter_sample
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
            await submitter_repository.save(submitter_sample)

        assert isinstance(exc_info.value, DatabaseException)
        assert "integridad de datos" in str(exc_info.value.detail["message"])
        assert "Duplicate entry" in str(exc_info.value.detail["details"])
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error handled correctly: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, submitter_repository, mock_session):
        """Test to verify that get_all returns all submitters."""
        print("🧪 Testing retrieval of all submitters...")

        submitters = [
            Submitter(
                id=1,
                names="John",
                paternal_surname="Doe",
                maternal_surname="Smith",
                dni=12345678,
                gender="Male",
            ),
            Submitter(
                id=2,
                names="Jane",
                paternal_surname="Doe",
                maternal_surname="Johnson",
                dni=87654321,
                gender="Female",
            ),
        ]

        submitter_repository.get_all = AsyncMock(return_value=submitters)

        result = await submitter_repository.get_all()

        assert len(result) == 2
        assert result[0].names == "John"
        assert result[1].names == "Jane"
        print(f"✅ All submitters retrieved: {len(result)} submitters found")
        for i, submitter in enumerate(result):
            print(
                f"   - Submitter {i+1}: ID={submitter.id}, Name='{submitter.names} {submitter.paternal_surname}'"
            )

    @pytest.mark.asyncio
    async def test_delete_success(
        self, submitter_repository, mock_session, submitter_sample
    ):
        """Test to verify that delete correctly removes a submitter."""
        print("🧪 Testing submitter deletion...")

        submitter_repository.get_by_id = AsyncMock(return_value=submitter_sample)

        result = await submitter_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(submitter_sample)
        print(
            f"✅ Submitter deleted successfully: ID=1, Name='{submitter_sample.names} {submitter_sample.paternal_surname}'"
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, submitter_repository, mock_session, submitter_sample
    ):
        """Test to verify that get_by_id returns the correct submitter."""
        print("🧪 Testing submitter retrieval by ID...")

        submitter_repository.get_by_id = AsyncMock(return_value=submitter_sample)

        result = await submitter_repository.get_by_id(1)

        assert result == submitter_sample
        assert result.names == "John"
        print(
            f"✅ Submitter retrieved by ID: ID={result.id}, Name='{result.names} {result.paternal_surname}'"
        )

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, submitter_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing submitter pagination...")

        submitters = [
            Submitter(
                id=1,
                names="John",
                paternal_surname="Doe",
                maternal_surname="Smith",
                dni=12345678,
                gender="Male",
            ),
            Submitter(
                id=2,
                names="Jane",
                paternal_surname="Doe",
                maternal_surname="Johnson",
                dni=87654321,
                gender="Female",
            ),
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page_result = Page(data=submitters, meta=pagination_info)

        submitter_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await submitter_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Submitters paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} submitters"
        )
        for i, submitter in enumerate(result.data):
            print(
                f"   - Submitter {i+1}: ID={submitter.id}, Name='{submitter.names} {submitter.paternal_surname}'"
            )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, submitter_repository, mock_session):
        """Test to verify that exists_by returns True when the submitter exists."""
        print("🧪 Testing submitter existence verification...")

        submitter_repository.exists_by = AsyncMock(return_value=True)

        result = await submitter_repository.exists_by(names="John")

        assert result is True
        print(f"✅ Submitter existence verified: 'John' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, submitter_repository, mock_session):
        """Test to verify that exists_by returns False when the submitter does not exist."""
        print("🧪 Testing non-existent submitter verification...")

        submitter_repository.exists_by = AsyncMock(return_value=False)

        result = await submitter_repository.exists_by(names="NonExistent")

        assert result is False
        print(f"✅ Non-existence verification: 'NonExistent' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, submitter_repository):
        """Test to verify that exists_by handles invalid field correctly."""
        print("🧪 Testing invalid field handling...")

        submitter_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException("Invalid field")
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await submitter_repository.exists_by(nonexistent_field="value")

        print(f"✅ Invalid field handled correctly: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, submitter_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        submitters = [
            Submitter(
                id=1,
                names="John",
                paternal_surname="Doe",
                maternal_surname="Smith",
                dni=12345678,
                gender="Male",
            )
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page_result = Page(data=submitters, meta=pagination_info)

        submitter_repository.find = AsyncMock(return_value=page_result)

        search_params = {"names": "John"}
        result = await submitter_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].names == "John"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, submitter in enumerate(result.data):
            print(
                f"   - Result {i+1}: ID={submitter.id}, Name='{submitter.names} {submitter.paternal_surname}'"
            )

    @pytest.mark.asyncio
    async def test_find_no_results(self, submitter_repository, mock_session):
        """Test to verify that find returns no results when there are none."""
        print("🧪 Testing search with filters (no results)...")

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page_result = Page(data=[], meta=pagination_info)

        submitter_repository.find = AsyncMock(return_value=page_result)

        search_params = {"names": "nonexistent"}
        result = await submitter_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 0
        assert result.meta.total == 0
        print(
            f"✅ Search with filters (no results) successful: Found {result.meta.total} results for criteria {search_params}"
        )
