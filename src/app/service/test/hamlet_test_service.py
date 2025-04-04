import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Hamlet
from src.app.dto.request import HamletRequestDTO
from src.app.dto.response import HamletResponseDTO, HamletPage
from src.app.service.implementations import HamletServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestHamletServiceImpl:
    @pytest.fixture
    def hamlet_repository(self):
        """
        Creates a mock repository for testing the hamlet service.

        :return: A mock hamlet repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def settlement_repository(self):
        """
        Creates a mock settlement repository for testing the hamlet service.

        :return: A mock settlement repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def hamlet_service(self, hamlet_repository, settlement_repository):
        """
        Creates a hamlet service instance for testing.

        :param hamlet_repository: The mock hamlet repository to inject
        :param settlement_repository: The mock settlement repository to inject
        :return: An instance of HamletServiceImpl with the mock repositories
        """
        return HamletServiceImpl(
            hamlet_repository=hamlet_repository,
            settlement_repository=settlement_repository,
        )

    @pytest.fixture
    def hamlet_request_dto(self):
        """
        Creates a sample hamlet request DTO.

        :return: A HamletRequestDTO instance with test data
        """
        return HamletRequestDTO(
            name="San Miguel",
            settlement_id=1,
        )

    @pytest.fixture
    def hamlet_entity(self):
        """
        Creates a sample hamlet entity.

        :return: A Hamlet instance with test data
        """
        return Hamlet(
            id=1,
            name="San Miguel",
            settlement_id=1,
            created_at=datetime.now(),
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_add_hamlet_success(
        self,
        hamlet_service,
        hamlet_repository,
        settlement_repository,
        hamlet_request_dto,
        hamlet_entity,
    ):
        """
        Tests successful hamlet creation.
        """
        print(f"\n🔹 Creating new hamlet: '{hamlet_request_dto.name}' 🔹")

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=False)
        settlement_repository.exists_by = AsyncMock(return_value=True)
        hamlet_repository.save = AsyncMock(return_value=hamlet_entity)

        # Execute test
        result = await hamlet_service.add_hamlet(hamlet_request_dto)
        print(f"✅ Hamlet successfully created with ID: {result.id}")

        # Verify results
        assert isinstance(result, HamletResponseDTO)
        assert result.id == hamlet_entity.id
        assert result.name == hamlet_entity.name
        assert result.settlement_id == hamlet_entity.settlement_id

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(
            name=hamlet_request_dto.name
        )
        settlement_repository.exists_by.assert_called_once_with(
            id=hamlet_request_dto.settlement_id
        )
        hamlet_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_hamlet_name_conflict(
        self, hamlet_service, hamlet_repository, hamlet_request_dto
    ):
        """
        Tests hamlet creation with a name that already exists.
        """
        print(
            f"\n🔹 Attempting to create hamlet with existing name: '{hamlet_request_dto.name}' 🔹"
        )

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=True)

        # Execute test and verify exception
        with pytest.raises(ConflictException) as exc_info:
            await hamlet_service.add_hamlet(hamlet_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        # Verify the exception message
        assert f"Hamlet with name {hamlet_request_dto.name} already exists" in str(
            exc_info.value
        )

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(
            name=hamlet_request_dto.name
        )
        hamlet_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_hamlet_settlement_not_found(
        self,
        hamlet_service,
        hamlet_repository,
        settlement_repository,
        hamlet_request_dto,
    ):
        """
        Tests hamlet creation with a non-existent settlement ID.
        """
        print(
            f"\n🔹 Attempting to create hamlet with non-existent settlement ID: {hamlet_request_dto.settlement_id} 🔹"
        )

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=False)
        settlement_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await hamlet_service.add_hamlet(hamlet_request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert (
            f"Settlement with ID {hamlet_request_dto.settlement_id} does not exist"
            in str(exc_info.value)
        )

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(
            name=hamlet_request_dto.name
        )
        settlement_repository.exists_by.assert_called_once_with(
            id=hamlet_request_dto.settlement_id
        )
        hamlet_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_hamlets(
        self, hamlet_service, hamlet_repository, hamlet_entity
    ):
        """
        Tests retrieving all hamlets.
        """
        print("\n🔹 Getting all hamlets 🔍")

        # Create test data
        hamlets = [
            hamlet_entity,
            Hamlet(
                id=2,
                name="El Paraíso",
                settlement_id=2,
                created_at=datetime.now(),
                updated_at=None,
            ),
        ]

        # Configure mocks
        hamlet_repository.get_all = AsyncMock(return_value=hamlets)

        # Execute test
        result = await hamlet_service.get_all_hamlets()
        print(f"📋 Found {len(result)} hamlets")

        # Verify results
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(hamlet, HamletResponseDTO) for hamlet in result)
        assert result[0].id == 1
        assert result[0].name == "San Miguel"
        assert result[1].id == 2
        assert result[1].name == "El Paraíso"

        # Verify method calls
        hamlet_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_hamlet_success(
        self,
        hamlet_service,
        hamlet_repository,
        settlement_repository,
        hamlet_entity,
    ):
        """
        Tests successful hamlet update.
        """
        print(f"\n🔹 Updating hamlet ID: 1 🔄")

        # Create updated request
        updated_request = HamletRequestDTO(
            name="San Miguel Actualizado",
            settlement_id=1,
        )

        # Create updated entity
        updated_entity = Hamlet(
            id=1,
            name="San Miguel Actualizado",
            settlement_id=1,
            created_at=hamlet_entity.created_at,
            updated_at=datetime.now(),
        )

        # Configure mocks - el nombre actualizado NO existe ya en otro hamlet
        hamlet_repository.exists_by = AsyncMock(
            side_effect=lambda **kwargs: True if 'id' in kwargs else False
        )
        hamlet_repository.get_by_id = AsyncMock(return_value=hamlet_entity)
        settlement_repository.exists_by = AsyncMock(return_value=True)
        hamlet_repository.save = AsyncMock(return_value=updated_entity)

        # Execute test
        result = await hamlet_service.update_hamlet(1, updated_request)
        print(f"✅ Hamlet successfully updated: {result.name}")

        # Verify results
        assert isinstance(result, HamletResponseDTO)
        assert result.id == 1
        assert result.name == "San Miguel Actualizado"
        assert result.updated_at is not None

        # Verify method calls
        hamlet_repository.exists_by.assert_any_call(id=1)
        hamlet_repository.get_by_id.assert_called_once_with(1)
        settlement_repository.exists_by.assert_called_once_with(
            id=updated_request.settlement_id
        )
        hamlet_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_hamlet_not_found(self, hamlet_service, hamlet_repository):
        """
        Tests hamlet update when the hamlet doesn't exist.
        """
        print(f"\n🔹 Attempting to update non-existent hamlet (ID: 999) 🔄")

        # Create update request
        updated_request = HamletRequestDTO(
            name="San Miguel Actualizado",
            settlement_id=1,
        )

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await hamlet_service.update_hamlet(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Hamlet with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(id=999)
        hamlet_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_hamlet_name_conflict(
        self, hamlet_service, hamlet_repository, hamlet_entity
    ):
        """
        Tests hamlet update with a conflicting name.
        """
        print(f"\n🔹 Attempting to update hamlet to a name already in use 🔄")

        # Create update request with new name
        updated_request = HamletRequestDTO(
            name="El Paraíso",  # Different from current name
            settlement_id=1,
        )

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(
            side_effect=[True, True]
        )  # ID exists, name exists
        hamlet_repository.get_by_id = AsyncMock(return_value=hamlet_entity)

        # Execute test and verify exception
        with pytest.raises(ConflictException) as exc_info:
            await hamlet_service.update_hamlet(1, updated_request)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        # Verify the exception message
        assert f"Hamlet with name {updated_request.name} already exists" in str(
            exc_info.value
        )

        # Verify method calls
        hamlet_repository.exists_by.assert_any_call(id=1)
        hamlet_repository.exists_by.assert_any_call(name=updated_request.name)
        hamlet_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_hamlet_success(self, hamlet_service, hamlet_repository):
        """
        Tests successful hamlet deletion.
        """
        print("\n🔹 Deleting hamlet (ID: 1) 🗑️")

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=True)
        hamlet_repository.delete = AsyncMock(return_value=True)

        # Execute test
        result = await hamlet_service.delete_hamlet(1)
        print(f"✅ {result.message}")

        # Verify results
        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Hamlet deleted successfully" in result.message

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(id=1)
        hamlet_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_hamlet_not_found(self, hamlet_service, hamlet_repository):
        """
        Tests hamlet deletion when the hamlet doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent hamlet (ID: 999) 🗑️")

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await hamlet_service.delete_hamlet(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Hamlet with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(id=999)
        hamlet_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_hamlet_by_id_success(
        self, hamlet_service, hamlet_repository, hamlet_entity
    ):
        """
        Tests retrieving a hamlet by ID.
        """
        print("\n🔹 Finding hamlet by ID: 1 🔍")

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=True)
        hamlet_repository.get_by_id = AsyncMock(return_value=hamlet_entity)

        # Execute test
        result = await hamlet_service.get_hamlet_by_id(1)
        print(f"✅ Hamlet found: '{result.name}'")

        # Verify results
        assert isinstance(result, HamletResponseDTO)
        assert result.id == 1
        assert result.name == "San Miguel"

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(id=1)
        hamlet_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_hamlet_by_id_not_found(self, hamlet_service, hamlet_repository):
        """
        Tests retrieving a non-existent hamlet by ID.
        """
        print("\n🔹 Finding non-existent hamlet by ID: 999 🔍")

        # Configure mocks
        hamlet_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await hamlet_service.get_hamlet_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Hamlet with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        hamlet_repository.exists_by.assert_called_once_with(id=999)
        hamlet_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_hamlets_paginated_success(
        self, hamlet_service, hamlet_repository, hamlet_entity
    ):
        """
        Tests retrieving paginated hamlets.
        """
        print("\n🔹 Getting hamlets with pagination (page: 1, size: 10) 📄")

        hamlets_data = [
            {
                "id": 1,
                "name": "San Miguel",
                "settlement_id": 1,
                "settlement_name": "Central Settlement",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "name": "El Paraíso",
                "settlement_id": 2,
                "settlement_name": "Northern Settlement",
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
        page_result = Page(data=hamlets_data, meta=pagination)

        hamlet_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await hamlet_service.get_hamlets_paginated(page=1, size=10)
        print(
            f"📋 Página {result.meta.current_page} de {result.meta.total_pages}, {len(result.data)} resultados de {result.meta.total} en total"
        )

        assert isinstance(result, HamletPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1

        hamlet_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_get_hamlets_paginated_invalid_params(self, hamlet_service):
        """
        Tests retrieving paginated hamlets with invalid parameters.
        """
        print("\n🔹 Testing pagination with invalid parameters ⚠️")

        # Test invalid page number
        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await hamlet_service.get_hamlets_paginated(page=0, size=10)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        # Test invalid size number
        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await hamlet_service.get_hamlets_paginated(page=1, size=0)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_success(self, hamlet_service, hamlet_repository, hamlet_entity):
        """
        Tests searching for hamlets with filter criteria.
        """
        print("\n🔹 Searching for hamlets with search criteria 🔍")

        hamlets_data = [
            {
                "id": 1,
                "name": "San Miguel",
                "settlement_id": 1,
                "settlement_name": "Central Settlement",
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
        page_result = Page(data=hamlets_data, meta=pagination)

        hamlet_repository.find = AsyncMock(return_value=page_result)

        search_term = "San Miguel"

        result = await hamlet_service.find(page=1, size=10, search_term=search_term)
        print(f"🔎 Found {len(result.data)} hamlets matching search criteria")

        assert isinstance(result, HamletPage)
        assert len(result.data) == 1
        assert result.data[0].name == "San Miguel"
        assert result.meta.total == 1

        hamlet_repository.find.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_not_found(self, hamlet_service, hamlet_repository):
        """
        Tests searching for hamlets when none are found.
        """
        print("\n🔹 Searching for non-existent hamlets 🔍")

        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=[], meta=pagination)

        hamlet_repository.find = AsyncMock(return_value=page_result)

        search_term = "NotFound"

        with pytest.raises(NotFoundException) as exc_info:
            await hamlet_service.find(page=1, size=10, search_term=search_term)
        print(f"⚠️ Expected error: {exc_info.value}")

        assert f"No hamlets found with the search term {search_term}" in str(
            exc_info.value
        )

        hamlet_repository.find.assert_called_once()
