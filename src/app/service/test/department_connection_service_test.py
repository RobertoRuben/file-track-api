import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from pydantic import ValidationError
from src.app.dto.request import DepartmentConnectionRequestDTO
from src.app.dto.response import (
    DepartmentConnectionResponseDTO,
    DepartmentConnectionPage,
)
from src.app.service.implementations import DepartmentConnectionServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestDepartmentConnectionServiceImpl:
    @pytest.fixture
    def department_connection_repository(self):
        """
        Creates a mock repository for testing the department connection service.

        :return: A mock department connection repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def department_repository(self):
        """
        Creates a mock department repository for testing the department connection service.

        :return: A mock department repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def department_connection_service(
        self, department_connection_repository, department_repository
    ):
        """
        Creates a department connection service instance for testing.

        :param department_connection_repository: The mock department connection repository to inject
        :param department_repository: The mock department repository to inject
        :return: An instance of DepartmentConnectionServiceImpl with the mock repositories
        """
        return DepartmentConnectionServiceImpl(
            department_connection_repository=department_connection_repository,
            department_repository=department_repository,
        )

    @pytest.fixture
    def department_connection_request_dto(self):
        """
        Creates a sample department connection request DTO.

        :return: A DepartmentConnectionRequestDTO instance with test data
        """
        return DepartmentConnectionRequestDTO(
            source_department_id=1,
            target_department_id=2,
        )

    @pytest.fixture
    def department_connection_entity(self):
        """
        Creates a sample department connection entity.

        :return: A MagicMock instance simulating a DepartmentConnection object for testing
        """
        connection = MagicMock()
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

    @pytest.mark.asyncio
    async def test_add_department_connection_success(
        self,
        department_connection_service,
        department_connection_repository,
        department_repository,
        department_connection_request_dto,
        department_connection_entity,
    ):
        """
        Tests successful department connection creation.
        """
        print(
            f"\n🔹 Creating new department connection: Source={department_connection_request_dto.source_department_id}, "
            f"Target={department_connection_request_dto.target_department_id} 🔹"
        )

        # Configure mocks to ensure departments exist before creating a connection
        department_repository.exists_by = AsyncMock(return_value=True)
        department_connection_repository.exists_by = AsyncMock(return_value=False)
        department_connection_repository.save = AsyncMock(
            return_value=department_connection_entity
        )

        # Mock saving departments if they don't already exist (just for simulation)
        department_repository.save = AsyncMock(
            side_effect=lambda department: department
        )

        # Ensure both departments exist before creating the connection
        source_department = MagicMock()
        source_department.id = department_connection_request_dto.source_department_id
        source_department.name = "Source Department"

        target_department = MagicMock()
        target_department.id = department_connection_request_dto.target_department_id
        target_department.name = "Target Department"

        # Simulate saving departments to the repository
        await department_repository.save(source_department)
        await department_repository.save(target_department)

        # Execute test for adding department connection
        result = await department_connection_service.add_department_connection(
            department_connection_request_dto
        )
        print(f"✅ Department connection successfully created with ID: {result.id}")

        # Verify results
        assert isinstance(result, DepartmentConnectionResponseDTO)
        assert result.id == department_connection_entity.id
        assert (
            result.source_department_id
            == department_connection_entity.source_department_id
        )
        assert (
            result.target_department_id
            == department_connection_entity.target_department_id
        )

        # Verify method calls
        department_repository.exists_by.assert_any_call(
            id=department_connection_request_dto.source_department_id
        )
        department_repository.exists_by.assert_any_call(
            id=department_connection_request_dto.target_department_id
        )
        department_connection_repository.save.assert_called_once()

        # Ensure departments were saved before creating the connection
        department_repository.save.assert_any_call(source_department)
        department_repository.save.assert_any_call(target_department)

    @pytest.mark.asyncio
    async def test_add_department_connection_same_departments(
        self, department_connection_service
    ):
        """
        Tests validation that prevents creating department connections with same source and target departments.
        """
        print(
            "\n🔹 Validating department connection with same source and target departments 🔹"
        )

        # Verify that the DTO correctly rejects equal values
        with pytest.raises(ValidationError) as validation_error:
            DepartmentConnectionRequestDTO(
                source_department_id=1, target_department_id=1
            )

        # Verify the error message
        error_detail = str(validation_error.value)
        print(f"✅ Validation correctly prevented equal departments: {error_detail}")
        assert "Source and target departments cannot be the same" in error_detail

    @pytest.mark.asyncio
    async def test_add_department_connection_source_not_found(
        self,
        department_connection_service,
        department_connection_repository,
        department_repository,
    ):
        """
        Tests department connection creation with non-existent source department.
        """
        print(
            "\n🔹 Attempting to create department connection with non-existent source department 🔹"
        )

        request_dto = DepartmentConnectionRequestDTO(
            source_department_id=999, target_department_id=2
        )

        # Configure mocks
        department_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await department_connection_service.add_department_connection(request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Department with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        department_repository.exists_by.assert_called_once_with(id=999)
        department_connection_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_department_connection_target_not_found(
        self,
        department_connection_service,
        department_connection_repository,
        department_repository,
    ):
        """
        Tests department connection creation with non-existent target department.
        """
        print(
            "\n🔹 Attempting to create department connection with non-existent target department 🔹"
        )

        request_dto = DepartmentConnectionRequestDTO(
            source_department_id=1, target_department_id=999
        )

        # Configure mocks
        department_repository.exists_by = AsyncMock(side_effect=[True, False])

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await department_connection_service.add_department_connection(request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Department with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        department_repository.exists_by.assert_any_call(id=1)
        department_repository.exists_by.assert_any_call(id=999)
        department_connection_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_department_connection_already_exists(
        self,
        department_connection_service,
        department_connection_repository,
        department_repository,
    ):
        """
        Tests department connection creation when the connection already exists.
        """
        print("\n🔹 Attempting to create duplicate department connection 🔹")

        request_dto = DepartmentConnectionRequestDTO(
            source_department_id=1, target_department_id=2
        )

        # Configure mocks
        department_repository.exists_by = AsyncMock(return_value=True)
        department_connection_repository.exists_by = AsyncMock(return_value=True)

        # Execute test and verify exception
        with pytest.raises(ConflictException) as exc_info:
            await department_connection_service.add_department_connection(request_dto)

        print(f"⚠️ Conflict detected: {exc_info.value}")

        # Verify the exception message
        assert (
            "Department connection already exists between department 1 and department 2"
            in str(exc_info.value)
        )

        # Verify method calls
        department_connection_repository.exists_by.assert_called_once()
        department_connection_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_department_connections(
        self, department_connection_service, department_connection_repository
    ):
        """
        Tests retrieving all department connections.
        """
        print("\n🔹 Getting all department connections 🔍")

        # Create test data
        connection1 = MagicMock()
        connection1.id = 1
        connection1.source_department_id = 1
        connection1.target_department_id = 2
        connection1.source_department = MagicMock(id=1, name="Department 1")
        connection1.target_department = MagicMock(id=2, name="Department 2")
        connection1.created_at = datetime.now()
        connection1.updated_at = None

        connection2 = MagicMock()
        connection2.id = 2
        connection2.source_department_id = 2
        connection2.target_department_id = 3
        connection2.source_department = MagicMock(id=2, name="Department 2")
        connection2.target_department = MagicMock(id=3, name="Department 3")
        connection2.created_at = datetime.now()
        connection2.updated_at = None

        connections = [connection1, connection2]

        # Configure mocks
        department_connection_repository.get_all = AsyncMock(return_value=connections)

        # Execute test
        result = await department_connection_service.get_all_department_connections()
        print(f"📋 Found {len(result)} connections")

        # Verify results
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(conn, DepartmentConnectionResponseDTO) for conn in result)
        assert result[0].id == 1
        assert result[0].source_department_id == 1
        assert result[1].id == 2
        assert result[1].source_department_id == 2

        # Verify method calls
        department_connection_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_department_connection_success(
        self,
        department_connection_service,
        department_connection_repository,
        department_repository,
        department_connection_entity,
    ):
        """
        Tests successful department connection update.
        """
        print(f"\n🔹 Updating department connection ID: 1 🔄")

        # Create updated request
        updated_request = DepartmentConnectionRequestDTO(
            source_department_id=3,
            target_department_id=4,
        )

        # Create updated entity
        updated_entity = MagicMock()
        updated_entity.id = 1
        updated_entity.source_department_id = 3
        updated_entity.target_department_id = 4
        updated_entity.created_at = department_connection_entity.created_at
        updated_entity.updated_at = datetime.now()
        updated_entity.source_department = MagicMock(id=3, name="Department 3")
        updated_entity.target_department = MagicMock(id=4, name="Department 4")

        # Configure mocks
        department_connection_repository.get_by_id = AsyncMock(
            return_value=department_connection_entity
        )
        department_repository.exists_by = AsyncMock(return_value=True)
        department_connection_repository.exists_by = AsyncMock(return_value=False)
        department_connection_repository.save = AsyncMock(return_value=updated_entity)

        # Execute test
        result = await department_connection_service.update_department_connection(
            1, updated_request
        )
        print(
            f"✅ Department connection successfully updated: Source={result.source_department_id}, Target={result.target_department_id}"
        )

        # Verify results
        assert isinstance(result, DepartmentConnectionResponseDTO)
        assert result.id == 1
        assert result.source_department_id == 3
        assert result.target_department_id == 4
        assert result.updated_at is not None

        # Verify method calls
        department_connection_repository.get_by_id.assert_called_once_with(1)
        department_repository.exists_by.assert_any_call(
            id=updated_request.source_department_id
        )
        department_repository.exists_by.assert_any_call(
            id=updated_request.target_department_id
        )
        department_connection_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_department_connection_not_found(
        self,
        department_connection_service,
        department_connection_repository,
        department_repository,
    ):
        """
        Tests department connection update when the connection doesn't exist.
        """
        print(
            f"\n🔹 Attempting to update non-existent department connection (ID: 999) 🔄"
        )

        # Create update request
        updated_request = DepartmentConnectionRequestDTO(
            source_department_id=3,
            target_department_id=4,
        )

        # Configure mocks
        department_repository.exists_by = AsyncMock(return_value=True)
        department_connection_repository.exists_by = AsyncMock(return_value=False)
        department_connection_repository.get_by_id = AsyncMock(
            side_effect=NotFoundException(
                details="Department connection with ID 999 not found."
            )
        )

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await department_connection_service.update_department_connection(
                999, updated_request
            )
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Department connection with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        department_repository.exists_by.assert_any_call(id=3)
        department_repository.exists_by.assert_any_call(id=4)
        department_connection_repository.get_by_id.assert_called_once_with(999)
        department_connection_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_department_connection_success(
        self, department_connection_service, department_connection_repository
    ):
        """
        Tests successful department connection deletion.
        """
        print("\n🔹 Deleting department connection (ID: 1) 🗑️")

        # Configure mocks
        department_connection_repository.exists_by = AsyncMock(return_value=True)
        department_connection_repository.delete = AsyncMock(return_value=True)

        # Execute test
        result = await department_connection_service.delete_department_connection(1)
        print(f"✅ {result.detail}")

        # Verify results
        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Department connection deleted successfully" in result.message

        # Verify method calls
        department_connection_repository.exists_by.assert_called_once_with(id=1)
        department_connection_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_department_connection_not_found(
        self, department_connection_service, department_connection_repository
    ):
        """
        Tests department connection deletion when the connection doesn't exist.
        """
        print(
            "\n🔹 Attempting to delete non-existent department connection (ID: 999) 🗑️"
        )

        # Configure mocks
        department_connection_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await department_connection_service.delete_department_connection(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Department connection with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        department_connection_repository.exists_by.assert_called_once_with(id=999)
        department_connection_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_department_connection_by_id_success(
        self,
        department_connection_service,
        department_connection_repository,
        department_connection_entity,
    ):
        """
        Tests retrieving a department connection by ID.
        """
        print("\n🔹 Finding department connection by ID: 1 🔍")

        # Configure mocks
        department_connection_repository.exists_by = AsyncMock(return_value=True)
        department_connection_repository.get_by_id = AsyncMock(
            return_value=department_connection_entity
        )

        # Execute test
        result = await department_connection_service.get_department_connection_by_id(1)
        print(
            f"✅ Department connection found: Source={result.source_department_id}, Target={result.target_department_id}"
        )

        # Verify results
        assert isinstance(result, DepartmentConnectionResponseDTO)
        assert result.id == 1
        assert result.source_department_id == 1
        assert result.target_department_id == 2

        # Verify method calls
        department_connection_repository.exists_by.assert_called_once_with(id=1)
        department_connection_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_department_connection_by_id_invalid_id(
        self, department_connection_service
    ):
        """
        Tests retrieving a department connection with an invalid ID.
        """
        print("\n🔹 Attempting to find department connection with invalid ID: -1 🔍")

        # Execute test and verify exception
        with pytest.raises(BadRequestException) as exc_info:
            await department_connection_service.get_department_connection_by_id(-1)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Department connection ID must be greater than or equal to 0" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_get_department_connection_by_id_not_found(
        self, department_connection_service, department_connection_repository
    ):
        """
        Tests retrieving a non-existent department connection by ID.
        """
        print("\n🔹 Finding non-existent department connection by ID: 999 🔍")

        # Configure mocks
        department_connection_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await department_connection_service.get_department_connection_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Department connection with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        department_connection_repository.exists_by.assert_called_once_with(id=999)
        department_connection_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_paginated_department_connections_success(
        self, department_connection_service, department_connection_repository
    ):
        """
        Tests retrieving paginated department connections.
        """
        print(
            "\n🔹 Getting department connections with pagination (page: 1, size: 10) 📄"
        )

        connections_data = [
            {
                "id": 1,
                "source_department_id": 1,
                "target_department_id": 2,
                "source_department_name": "Department 1",
                "target_department_name": "Department 2",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "source_department_id": 2,
                "target_department_id": 3,
                "source_department_name": "Department 2",
                "target_department_name": "Department 3",
                "created_at": datetime.now(),
                "updated_at": None,
            },
        ]

        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=connections_data, meta=pagination)

        department_connection_repository.get_pageable = AsyncMock(
            return_value=page_result
        )

        result = (
            await department_connection_service.get_paginated_department_connections(
                page=1, size=10
            )
        )
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} in total"
        )

        assert isinstance(result, DepartmentConnectionPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1

        department_connection_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_find_department_connections_success(
        self, department_connection_service, department_connection_repository
    ):
        """
        Tests searching for department connections with specific criteria.
        """
        print("\n🔹 Searching for department connections with term: 'Department 1' 🔍")

        connections_data = [
            {
                "id": 1,
                "source_department_id": 1,
                "target_department_id": 2,
                "source_department_name": "Department 1",
                "target_department_name": "Department 2",
                "created_at": datetime.now(),
                "updated_at": None,
            }
        ]

        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=connections_data, meta=pagination)

        department_connection_repository.find = AsyncMock(return_value=page_result)

        result = await department_connection_service.find(
            page=1, size=10, search_term="Department 1"
        )
        print(f"📋 Found {len(result.data)} connections matching search criteria")

        assert isinstance(result, DepartmentConnectionPage)
        assert len(result.data) == 1
        assert result.data[0].source_department_name == "Department 1"

        # Verify search was performed with correct parameters
        department_connection_repository.find.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_connections_by_source_department_id_success(
        self,
        department_connection_service,
        department_connection_repository,
        department_repository,
    ):
        """
        Tests retrieving connections by source department ID.
        """
        print("\n🔹 Getting connections by source department ID: 1 🔍")

        # Create test data
        connection1 = MagicMock()
        connection1.id = 1
        connection1.source_department_id = 1
        connection1.target_department_id = 2
        connection1.created_at = datetime.now()
        connection1.updated_at = None

        connection2 = MagicMock()
        connection2.id = 3
        connection2.source_department_id = 1
        connection2.target_department_id = 3
        connection2.created_at = datetime.now()
        connection2.updated_at = None

        connections = [connection1, connection2]

        # Configure mocks
        department_repository.exists_by = AsyncMock(return_value=True)
        department_connection_repository.get_connections_by_source_department_id = (
            AsyncMock(return_value=connections)
        )

        # Execute test
        result = (
            await department_connection_service.get_connections_by_source_department_id(
                1
            )
        )
        print(f"📋 Found {len(result)} connections for department ID: 1")

        # Verify results
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(conn, DepartmentConnectionResponseDTO) for conn in result)
        assert all(conn.source_department_id == 1 for conn in result)

        # Verify method calls
        department_repository.exists_by.assert_called_once_with(id=1)
        department_connection_repository.get_connections_by_source_department_id.assert_called_once_with(
            1
        )
