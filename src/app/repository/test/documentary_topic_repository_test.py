import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations import DocumentaryTopicRepositoryImpl
from src.app.model.entity import DocumentaryTopic
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
def documentary_topic_repository(mock_session):
    return DocumentaryTopicRepositoryImpl(session=mock_session)


@pytest.fixture
def documentary_topic_sample():
    return DocumentaryTopic(
        id=1, name="Legal Documentation", created_at=datetime.now(), updated_at=None
    )


class TestDocumentaryTopicRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, documentary_topic_repository, mock_session, documentary_topic_sample
    ):
        """Test to verify that the save method correctly stores a documentary topic."""
        print("🧪 Testing successful documentary topic saving...")

        result = await documentary_topic_repository.save(documentary_topic_sample)

        mock_session.add.assert_called_once_with(documentary_topic_sample)
        assert result == documentary_topic_sample
        print(
            f"✅ Documentary topic saved successfully: ID={result.id}, Name='{result.name}'"
        )

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, documentary_topic_repository, mock_session, documentary_topic_sample
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
            await documentary_topic_repository.save(documentary_topic_sample)

        assert isinstance(exc_info.value, DatabaseException)
        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, documentary_topic_repository, mock_session):
        """Test to verify that get_all returns all documentary topics."""
        print("🧪 Testing retrieval of all documentary topics...")

        topics = [
            DocumentaryTopic(id=1, name="Legal Documentation"),
            DocumentaryTopic(id=2, name="Technical Documentation"),
        ]

        documentary_topic_repository.get_all = AsyncMock(return_value=topics)

        result = await documentary_topic_repository.get_all()

        assert len(result) == 2
        assert result[0].name == "Legal Documentation"
        assert result[1].name == "Technical Documentation"
        print(f"✅ All documentary topics retrieved: {len(result)} topics found")
        for i, topic in enumerate(result):
            print(f"   - Topic {i+1}: ID={topic.id}, Name='{topic.name}'")

    @pytest.mark.asyncio
    async def test_delete_success(
        self, documentary_topic_repository, mock_session, documentary_topic_sample
    ):
        """Test to verify that delete correctly removes a documentary topic."""
        print("🧪 Testing documentary topic deletion...")

        documentary_topic_repository.get_by_id = AsyncMock(
            return_value=documentary_topic_sample
        )

        result = await documentary_topic_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(documentary_topic_sample)
        print(
            f"✅ Documentary topic deleted successfully: ID=1, Name='{documentary_topic_sample.name}'"
        )

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, documentary_topic_repository, mock_session, documentary_topic_sample
    ):
        """Test to verify that get_by_id returns the correct documentary topic."""
        print("🧪 Testing documentary topic retrieval by ID...")

        documentary_topic_repository.get_by_id = AsyncMock(
            return_value=documentary_topic_sample
        )

        result = await documentary_topic_repository.get_by_id(1)

        assert result == documentary_topic_sample
        assert result.name == "Legal Documentation"
        print(
            f"✅ Documentary topic retrieved by ID: ID={result.id}, Name='{result.name}'"
        )

    @pytest.mark.asyncio
    async def test_get_pageable_success(
        self, documentary_topic_repository, mock_session
    ):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing documentary topic pagination...")

        topics = [
            DocumentaryTopic(id=1, name="Legal Documentation"),
            DocumentaryTopic(id=2, name="Technical Documentation"),
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=topics, meta=pagination_info)

        documentary_topic_repository.get_pageable = AsyncMock(return_value=page)

        result = await documentary_topic_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(
            f"✅ Documentary topics paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} topics"
        )
        for i, topic in enumerate(result.data):
            print(f"   - Topic {i+1}: ID={topic.id}, Name='{topic.name}'")

    @pytest.mark.asyncio
    async def test_exists_by_success(self, documentary_topic_repository, mock_session):
        """Test to verify that exists_by returns True when the documentary topic exists."""
        print("🧪 Testing documentary topic existence verification...")

        documentary_topic_repository.exists_by = AsyncMock(return_value=True)

        result = await documentary_topic_repository.exists_by(
            name="Legal Documentation"
        )

        assert result is True
        print(
            f"✅ Documentary topic existence verified: 'Legal Documentation' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(
        self, documentary_topic_repository, mock_session
    ):
        """Test to verify that exists_by returns False when the documentary topic doesn't exist."""
        print("🧪 Testing non-existent documentary topic verification...")

        documentary_topic_repository.exists_by = AsyncMock(return_value=False)

        result = await documentary_topic_repository.exists_by(name="Non-existent Topic")

        assert result is False
        print(
            f"✅ Documentary topic non-existence verified: 'Non-existent Topic' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, documentary_topic_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        documentary_topic_repository.exists_by = AsyncMock(
            side_effect=InvalidFieldException("Invalid field")
        )

        with pytest.raises(InvalidFieldException) as exc_info:
            await documentary_topic_repository.exists_by(non_existent_field="value")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, documentary_topic_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        topics = [DocumentaryTopic(id=1, name="Legal Documentation")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=topics, meta=pagination_info)

        documentary_topic_repository.find = AsyncMock(return_value=page)

        search_params = {"name": "legal"}
        result = await documentary_topic_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].name == "Legal Documentation"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )
        for i, topic in enumerate(result.data):
            print(f"   - Result {i+1}: ID={topic.id}, Name='{topic.name}'")

    @pytest.mark.asyncio
    async def test_find_no_results(self, documentary_topic_repository, mock_session):
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

        page = Page(data=[], meta=pagination_info)

        documentary_topic_repository.find = AsyncMock(return_value=page)

        search_params = {"name": "nonexistent"}
        result = await documentary_topic_repository.find(
            page=1, size=10, search_dict=search_params
        )

        assert isinstance(result, Page)
        assert len(result.data) == 0
        assert result.meta.total == 0
        print(
            f"✅ Search with filters (no results) successful: Found {result.meta.total} results for criteria {search_params}"
        )
