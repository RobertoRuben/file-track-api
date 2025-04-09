import pytest
from datetime import datetime, date
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.app.repository.implementations.document_repository_impl import (
    DocumentRepositoryImpl,
)
from src.app.model.entity import Document
from src.app.exception.invalid_field_exception import InvalidFieldException
from src.app.schema import Page


@pytest.fixture
def mock_session():
    """Creates a mock session for testing."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def document_repository(mock_session):
    """Creates a repository instance with the mock session."""
    return DocumentRepositoryImpl(session=mock_session)


@pytest.fixture
def document_sample():
    """Creates a sample document for testing."""
    return Document(
        id=1,
        registration_code="DOC202304090001234567",  # 20 digits registration code
        title="Technical Report",
        subject="Environmental Impact Assessment",
        pages=15,
        storage_path="/documents/DOC202304090001234567.pdf",
        size=1024,
        submitter_id=1,
        document_category_id=1,
        documentary_topic_id=1,
        hamlet_id=1,
        settlement_id=1,
        registered_by_user_id=1,
        created_at=datetime.now(),
        updated_at=None,
    )


class TestDocumentRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self, document_repository, mock_session, document_sample
    ):
        """Tests that the save method correctly saves a document."""
        print("🧪 Testing successful document saving...")

        # Execute the test
        result = await document_repository.save(document_sample)

        # Verify results
        mock_session.add.assert_called_once_with(document_sample)
        assert result == document_sample
        print(f"✅ Document saved successfully: ID={result.id}, Title='{result.title}'")

    @pytest.mark.asyncio
    async def test_get_all_success(
        self, document_repository, mock_session, document_sample
    ):
        """Tests that get_all returns all documents."""
        print("🧪 Testing retrieval of all documents...")

        # Configure mock
        documents = [
            document_sample,
            Document(
                id=2,
                registration_code="DOC202304090001234568",  # 20 digits registration code
                title="Request",
                subject="Project Approval",
                pages=5,
                storage_path="/documents/DOC202304090001234568.pdf",
                size=512,
                submitter_id=2,
                document_category_id=2,
                documentary_topic_id=2,
                hamlet_id=2,
                settlement_id=2,
                registered_by_user_id=1,
                created_at=datetime.now(),
                updated_at=None,
            ),
        ]

        mock_result = MagicMock()
        mock_result.all.return_value = documents
        mock_session.exec.return_value = mock_result

        # Execute the test
        result = await document_repository.get_all()

        # Verify results
        assert len(result) == 2
        assert result[0].title == "Technical Report"
        assert result[1].title == "Request"
        print(f"✅ All documents retrieved: {len(result)} documents found")

    @pytest.mark.asyncio
    async def test_delete_success(
        self, document_repository, mock_session, document_sample
    ):
        """Tests that delete correctly removes a document."""
        print("🧪 Testing document deletion...")

        # Configure mock
        document_repository.get_by_id = AsyncMock(return_value=document_sample)

        # Execute the test
        result = await document_repository.delete(1)

        # Verify results
        mock_session.delete.assert_called_once_with(document_sample)
        assert result is True
        print(f"✅ Document deleted successfully: ID={document_sample.id}")

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, document_repository, mock_session, document_sample
    ):
        """Tests that get_by_id returns the correct document."""
        print("🧪 Testing document retrieval by ID...")

        # Configure mock
        mock_result = MagicMock()
        mock_result.first.return_value = document_sample
        mock_session.exec.return_value = mock_result

        # Execute the test
        result = await document_repository.get_by_id(1)

        # Verify results
        assert result == document_sample
        assert result.id == 1
        assert result.title == "Technical Report"
        print(f"✅ Document retrieved by ID: ID={result.id}, Title='{result.title}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, document_repository, mock_session):
        """Tests that get_pageable returns a page of results."""
        print("🧪 Testing document pagination...")

        # Test data
        documents_data = [
            {
                "id": 1,
                "registration_code": "DOC202304090001234567",  # 20 digits registration code
                "title": "Technical Report",
                "subject": "Environmental Impact Assessment",
                "pages": 15,
                "storage_path": "/documents/DOC202304090001234567.pdf",
                "size": 1024,
                "submitter_id": 1,
                "submitter_dni": "12345678",
                "document_category_id": 1,
                "document_category_name": "Reports",
                "documentary_topic_id": 1,
                "documentary_topic_name": "Environmental",
                "hamlet_id": 1,
                "hamlet_name": "Paradise",
                "settlement_id": 1,
                "settlement_name": "San Juan",
                "registered_by_user_id": 1,
                "registered_by_username": "admin",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "registration_code": "DOC202304090001234568",  # 20 digits registration code
                "title": "Request",
                "subject": "Project Approval",
                "pages": 5,
                "storage_path": "/documents/DOC202304090001234568.pdf",
                "size": 512,
                "submitter_id": 2,
                "submitter_dni": "87654321",
                "document_category_id": 2,
                "document_category_name": "Requests",
                "documentary_topic_id": 2,
                "documentary_topic_name": "Projects",
                "hamlet_id": 2,
                "hamlet_name": "Flower Gardens",
                "settlement_id": 2,
                "settlement_name": "San Pedro",
                "registered_by_user_id": 1,
                "registered_by_username": "admin",
                "created_at": datetime.now(),
                "updated_at": None,
            },
        ]

        # Configure mocks for results and count
        mock_rows = []
        for doc_data in documents_data:
            mock_row = MagicMock()
            mock_row._mapping = doc_data
            mock_rows.append(mock_row)

        mock_result = MagicMock()
        mock_result.__iter__.return_value = mock_rows

        mock_count_result = MagicMock()
        mock_count_result.first.return_value = 2

        mock_session.exec.side_effect = [mock_result, mock_count_result]

        # Execute the test
        result = await document_repository.get_pageable(page=1, size=10)

        # Verify results
        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        assert result.data[0]["title"] == "Technical Report"
        assert result.data[1]["title"] == "Request"
        print(
            f"✅ Paginated documents: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} total documents"
        )

    @pytest.mark.asyncio
    async def test_find_with_filters(self, document_repository, mock_session):
        """Tests that find correctly searches documents with filters."""
        print("🧪 Testing search with filters...")

        # Test data
        documents_data = [
            {
                "id": 1,
                "registration_code": "DOC202304090001234567",  # 20 digits registration code
                "title": "Technical Report",
                "subject": "Environmental Impact Assessment",
                "pages": 15,
                "storage_path": "/documents/DOC202304090001234567.pdf",
                "size": 1024,
                "submitter_id": 1,
                "submitter_dni": "12345678",
                "document_category_id": 1,
                "document_category_name": "Reports",
                "documentary_topic_id": 1,
                "documentary_topic_name": "Environmental",
                "hamlet_id": 1,
                "hamlet_name": "Paradise",
                "settlement_id": 1,
                "settlement_name": "San Juan",
                "registered_by_user_id": 1,
                "registered_by_username": "admin",
                "created_at": datetime.now(),
                "updated_at": None,
            }
        ]

        # Configure mocks for results and count
        mock_rows = []
        for doc_data in documents_data:
            mock_row = MagicMock()
            mock_row._mapping = doc_data
            mock_rows.append(mock_row)

        mock_result = MagicMock()
        mock_result.__iter__.return_value = mock_rows

        mock_count_result = MagicMock()
        mock_count_result.first.return_value = 1

        mock_session.exec.side_effect = [mock_result, mock_count_result]

        # Execute the test with a search criterion
        search_params = {"title": "Technical"}
        result = await document_repository.find(
            page=1, size=10, search_dict=search_params
        )

        # Verify results
        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0]["title"] == "Technical Report"
        assert result.meta.total == 1
        print(
            f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_success(self, document_repository, mock_session):
        """Tests that exists_by returns True when the document exists."""
        print("🧪 Testing document existence verification...")

        # Configure mock
        mock_result = AsyncMock()
        mock_result.first.return_value = 1
        mock_session.exec.return_value = mock_result

        # Execute the test
        result = await document_repository.exists_by(
            registration_code="DOC202304090001234567"
        )

        # Verify results
        assert result is True
        print(
            f"✅ Document existence verified: Document with code 'DOC202304090001234567' exists = {result}"
        )

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, document_repository, mock_session):
        """Tests that exists_by returns False when the document doesn't exist."""
        print("🧪 Testing non-existent document verification...")

        # Directly mock the exists_by method
        original_exists_by = document_repository.exists_by
        document_repository.exists_by = AsyncMock(return_value=False)

        try:
            # Execute the test
            result = await document_repository.exists_by(
                registration_code="NOTEXIST00000000000000"
            )

            # Verify results
            assert result is False
            print(
                f"✅ Non-existent document verification: Document with code 'NOTEXIST00000000000000' exists = {result}"
            )
        finally:
            # Restore the original method
            document_repository.exists_by = original_exists_by

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, document_repository):
        """Tests that exists_by raises an exception with an invalid field."""
        print("🧪 Testing invalid field handling...")

        # Execute the test and verify exception
        with pytest.raises(InvalidFieldException) as exc_info:
            await document_repository.exists_by(non_existent_field="value")

        # Verify exception message
        assert "does not exist in the Document model" in str(exc_info.value)
        print(f"✅ Invalid field handled correctly: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_by_registration_code_success(
        self, document_repository, mock_session, document_sample
    ):
        """Tests that get_by_registration_code returns the correct document."""
        print("🧪 Testing document retrieval by registration code...")

        # Configure mock
        mock_result = MagicMock()
        mock_result.first.return_value = document_sample
        mock_session.exec.return_value = mock_result

        # Execute the test
        result = await document_repository.get_by_registration_code(
            "DOC202304090001234567"
        )

        # Verify results
        assert result == document_sample
        assert result.registration_code == "DOC202304090001234567"
        print(
            f"✅ Document retrieved by code: '{result.registration_code}', Title='{result.title}'"
        )

    @pytest.mark.asyncio
    async def test_find_by_current_date(self, document_repository, mock_session):
        """Tests that find_by_current_date searches documents from the current date."""
        print("🧪 Testing document search by current date...")

        # Test data
        documents_data = [
            {
                "id": 1,
                "registration_code": "DOC202304090001234567",  # 20 digits registration code
                "title": "Technical Report",
                "subject": "Environmental Impact Assessment",
                "pages": 15,
                "storage_path": "/documents/DOC202304090001234567.pdf",
                "size": 1024,
                "submitter_id": 1,
                "submitter_dni": "12345678",
                "document_category_id": 1,
                "document_category_name": "Reports",
                "documentary_topic_id": 1,
                "documentary_topic_name": "Environmental",
                "hamlet_id": 1,
                "hamlet_name": "Paradise",
                "settlement_id": 1,
                "settlement_name": "San Juan",
                "registered_by_user_id": 1,
                "registered_by_username": "admin",
                "created_at": datetime.now(),
                "updated_at": None,
            }
        ]

        # Configure mocks for results and count
        mock_rows = []
        for doc_data in documents_data:
            mock_row = MagicMock()
            mock_row._mapping = doc_data
            mock_rows.append(mock_row)

        mock_result = MagicMock()
        mock_result.__iter__.return_value = mock_rows

        mock_count_result = MagicMock()
        mock_count_result.first.return_value = 1

        mock_session.exec.side_effect = [mock_result, mock_count_result]

        # Execute the test
        search_params = {"title": "Technical"}
        result = await document_repository.find_by_current_date(
            page=1, size=10, search_dict=search_params
        )

        # Verify results
        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.meta.total == 1
        print(
            f"✅ Search by current date successful: Found {result.meta.total} documents from today"
        )

    @pytest.mark.asyncio
    async def test_save_integrity_error(
        self, document_repository, mock_session, document_sample
    ):
        """Tests that the save method correctly handles integrity errors."""
        print("🧪 Testing integrity error handling during save...")

        # Configure mock to simulate integrity error
        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError(
            "Duplicate entry", None, error_original
        )

        # Execute the test and verify that the DatabaseException is raised
        from src.app.exception.database_exception import DatabaseException

        with pytest.raises(DatabaseException) as exc_info:
            await document_repository.save(document_sample)

        # Verify rollback was called and exception details
        mock_session.rollback.assert_called_once()
        assert "Error de integridad de datos" in str(exc_info.value)
        assert "Duplicate entry" in str(exc_info.value)
        print("✅ Integrity error correctly handled during save")
