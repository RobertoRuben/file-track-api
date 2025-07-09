import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from src.app.repository.implementations import DepartmentConnectionRepositoryImpl
from src.app.core.exception import InvalidFieldException
from src.app.model.entity import DepartmentConnection
from src.app.core.schema import Page


@pytest.fixture
def mock_session():
    """
    Creates a mock database session for testing.

    :return: A mock SQLAlchemy session with predefined async methods
    """
    session = MagicMock()
    session.exec = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.close = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def department_connection_repository(mock_session):
    """
    Creates a department connection repository instance for testing.

    :param mock_session: The mock database session to inject
    :return: An instance of DepartmentConnectionRepositoryImpl with the mock session
    """
    return DepartmentConnectionRepositoryImpl(mock_session)


@pytest.fixture
def department_connection_sample():
    """
    Creates a sample department connection entity for testing.

    :return: A mock department connection entity with test data
    """
    connection = MagicMock(spec=DepartmentConnection)
    connection.id = 1
    connection.source_department_id = 1
    connection.target_department_id = 2
    connection.created_at = datetime.now()
    connection.updated_at = None

    # Add properties for accessing relationships
    source_department = MagicMock()
    source_department.id = 1
    source_department.name = "Source Department"

    target_department = MagicMock()
    target_department.id = 2
    target_department.name = "Target Department"

    connection.source_department = source_department
    connection.target_department = target_department

    return connection


class TestDepartmentConnectionRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(
        self,
        department_connection_repository,
        mock_session,
        department_connection_sample,
    ):
        """Test to verify that the save method correctly stores a department connection."""
        print("🧪 Testing successful department connection saving...")

        # Execute test
        result = await department_connection_repository.save(
            department_connection_sample
        )

        # Verify results
        assert result == department_connection_sample
        mock_session.add.assert_called_once_with(department_connection_sample)

        print("✅ Department connection saved successfully")

    @pytest.mark.asyncio
    async def test_get_all_success(
        self,
        department_connection_repository,
        mock_session,
        department_connection_sample,
    ):
        """Test to verify that the get_all method correctly retrieves all department connections."""
        print("🧪 Testing successful retrieval of all department connections...")

        # Create second sample
        second_sample = MagicMock(spec=DepartmentConnection)
        second_sample.id = 2
        second_sample.source_department_id = 2
        second_sample.target_department_id = 3

        # Configure mock
        mock_exec_result = MagicMock()
        mock_exec_result.all = MagicMock(
            return_value=[department_connection_sample, second_sample]
        )
        mock_session.exec.return_value = mock_exec_result

        # Execute test
        result = await department_connection_repository.get_all()

        # Verify results
        assert len(result) == 2
        assert result[0] == department_connection_sample
        assert result[1] == second_sample
        mock_session.exec.assert_called_once()

        print(f"✅ Retrieved {len(result)} department connections")

    @pytest.mark.asyncio
    async def test_delete_success(
        self,
        department_connection_repository,
        mock_session,
        department_connection_sample,
    ):
        """Test to verify that the delete method correctly removes a department connection."""
        print("🧪 Testing successful department connection deletion...")

        # Configure mocks
        get_by_id_mock = AsyncMock(return_value=department_connection_sample)
        department_connection_repository.get_by_id = get_by_id_mock

        # Execute test
        result = await department_connection_repository.delete(1)

        # Verify results
        assert result is True
        department_connection_repository.get_by_id.assert_called_once_with(1)
        mock_session.delete.assert_called_once_with(department_connection_sample)

        print("✅ Department connection deleted successfully")

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self,
        department_connection_repository,
        mock_session,
        department_connection_sample,
    ):
        """Test to verify that the get_by_id method correctly retrieves a department connection."""
        print("🧪 Testing successful department connection retrieval by ID...")

        # Configure mock
        mock_exec_result = MagicMock()
        mock_exec_result.first = MagicMock(return_value=department_connection_sample)
        mock_session.exec.return_value = mock_exec_result

        # Execute test
        result = await department_connection_repository.get_by_id(1)

        # Verify results
        assert result == department_connection_sample
        mock_session.exec.assert_called_once()

        print("✅ Department connection retrieved successfully")

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self, department_connection_repository, mock_session
    ):
        """Test to verify behavior when a department connection is not found by ID."""
        print("🧪 Testing department connection not found by ID...")

        # Configure mock
        mock_exec_result = MagicMock()
        mock_exec_result.first = MagicMock(return_value=None)
        mock_session.exec.return_value = mock_exec_result

        # Execute test
        result = await department_connection_repository.get_by_id(999)

        # Verify results
        assert result is None
        mock_session.exec.assert_called_once()

        print("✅ Not found case handled correctly")

    @pytest.mark.asyncio
    async def test_get_pageable_success(
        self, department_connection_repository, mock_session
    ):
        """Test to verify that the get_pageable method correctly retrieves paginated department connections."""
        print("🧪 Testing successful paginated department connections retrieval...")

        # Create sample data
        connection_data = [
            {
                "id": 1,
                "source_department_id": 1,
                "target_department_id": 2,
                "created_at": datetime.now(),
                "updated_at": None,
                "source_department_name": "Source Dept",
                "target_department_name": "Target Dept",
            },
            {
                "id": 2,
                "source_department_id": 2,
                "target_department_id": 3,
                "created_at": datetime.now(),
                "updated_at": None,
                "source_department_name": "Another Source",
                "target_department_name": "Another Target",
            },
        ]

        # Configure mocks
        mock_row1 = MagicMock()
        mock_row1._mapping = connection_data[0]
        mock_row2 = MagicMock()
        mock_row2._mapping = connection_data[1]

        mock_data_result = MagicMock()
        mock_data_result.__iter__ = MagicMock(return_value=iter([mock_row1, mock_row2]))

        mock_count_result = MagicMock()
        mock_count_result.first = MagicMock(return_value=2)

        mock_session.exec = AsyncMock(side_effect=[mock_data_result, mock_count_result])

        # Execute test
        result = await department_connection_repository.get_pageable(1, 10)

        # Verify results
        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        assert result.meta.per_page == 10
        assert mock_session.exec.call_count == 2

        print(f"✅ Retrieved page with {len(result.data)} department connections")

    @pytest.mark.asyncio
    async def test_find_success(self, department_connection_repository, mock_session):
        """Test to verify that the find method correctly searches for department connections."""
        print("🧪 Testing successful department connection search...")

        # Create search dictionary
        search_dict = {"source_department_name": "Source"}

        # Create sample data matching search criteria
        connection_data = [
            {
                "id": 1,
                "source_department_id": 1,
                "target_department_id": 2,
                "created_at": datetime.now(),
                "updated_at": None,
                "source_department_name": "Source Dept",
                "target_department_name": "Target Dept",
            }
        ]

        # Configure mocks
        mock_row = MagicMock()
        mock_row._mapping = connection_data[0]

        mock_data_result = MagicMock()
        mock_data_result.__iter__ = MagicMock(return_value=iter([mock_row]))

        mock_count_result = MagicMock()
        mock_count_result.first = MagicMock(return_value=1)

        mock_session.exec = AsyncMock(side_effect=[mock_data_result, mock_count_result])

        # Execute test
        result = await department_connection_repository.find(1, 10, search_dict)

        # Verify results
        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.meta.total == 1
        assert mock_session.exec.call_count == 2

        print(f"✅ Search returned {len(result.data)} matching department connections")

    @pytest.mark.asyncio
    async def test_exists_by_success(
        self, department_connection_repository, mock_session
    ):
        """Test to verify that exists_by correctly checks for department connection existence."""
        print("🧪 Testing existence check for department connection...")

        # Configure mock
        mock_exec_result = MagicMock()
        mock_exec_result.first = MagicMock(return_value=1)  # ID was found
        mock_session.exec.return_value = mock_exec_result

        # Execute test
        result = await department_connection_repository.exists_by(id=1)

        # Verify results
        assert result is True
        mock_session.exec.assert_called_once()

        print("✅ Existence check successful")

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(
        self, department_connection_repository, mock_session
    ):
        """Test to verify behavior when checking existence with an invalid field."""
        print("🧪 Testing existence check with invalid field...")

        # Execute test
        with pytest.raises(InvalidFieldException) as exc_info:
            await department_connection_repository.exists_by(invalid_field="value")

        # Verify results
        assert "Field 'invalid_field' does not exist" in str(exc_info.value)

        print("✅ Invalid field exception correctly raised")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(
        self, department_connection_repository, mock_session
    ):
        """Test to verify behavior when checking existence of a non-existent department connection."""
        print("🧪 Testing existence check for non-existent department connection...")

        # Configure mock
        mock_exec_result = MagicMock()
        mock_exec_result.first = MagicMock(return_value=None)  # No ID found
        mock_session.exec.return_value = mock_exec_result

        # Execute test
        result = await department_connection_repository.exists_by(id=999)

        # Verify results
        assert result is False
        mock_session.exec.assert_called_once()

        print("✅ Non-existence correctly identified")

    @pytest.mark.asyncio
    async def test_get_connections_by_source_department_id(
        self,
        department_connection_repository,
        mock_session,
        department_connection_sample,
    ):
        """Test to verify retrieval of connections by source department ID."""
        print("🧪 Testing retrieval of connections by source department ID...")

        # Configure mock
        mock_exec_result = MagicMock()
        mock_exec_result.all = MagicMock(return_value=[department_connection_sample])
        mock_session.exec.return_value = mock_exec_result

        # Execute test
        result = await department_connection_repository.get_connections_by_source_department_id(
            1
        )

        # Verify results
        assert len(result) == 1
        assert result[0] == department_connection_sample
        mock_session.exec.assert_called_once()

        print(f"✅ Retrieved {len(result)} connections for source department ID 1")
