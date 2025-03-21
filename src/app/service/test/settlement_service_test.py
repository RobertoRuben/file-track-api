import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import CentroPoblado
from src.app.dto.request import SettlementRequestDTO
from src.app.dto.response import SettlementReponseDTO, SettlementPage
from src.app.service.implementations import SettlementServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestSettlementServiceImpl:
    @pytest.fixture
    def settlement_repository(self):
        """
        Creates a mock repository for testing the settlement service.

        Returns:
            A mock settlement repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def settlement_service(self, settlement_repository):
        """
        Creates a settlement service instance for testing.

        Args:
            settlement_repository: The mock repository to inject.

        Returns:
            An instance of SettlementServiceImpl with the mock repository.
        """
        return SettlementServiceImpl(repository=settlement_repository)

    @pytest.fixture
    def settlement_request_dto(self):
        """
        Creates a sample settlement request DTO.

        Returns:
            A SettlementRequestDTO instance with test data.
        """
        return SettlementRequestDTO(nombre="San Isidro")

    @pytest.fixture
    def settlement_entity(self):
        """
        Creates a sample settlement entity.

        Returns:
            A CentroPoblado instance with test data.
        """
        return CentroPoblado(
            id=1, nombre="San Isidro", created_at=datetime.now(), updated_at=None
        )

    @pytest.mark.asyncio
    async def test_add_settlement_success(
        self,
        settlement_service,
        settlement_repository,
        settlement_request_dto,
        settlement_entity,
    ):
        """
        Tests successful settlement creation.
        """
        print(f"\n🔹 Creating new settlement: '{settlement_request_dto.nombre}' 🔹")
        settlement_repository.exists_by = AsyncMock(return_value=False)
        settlement_repository.save = AsyncMock(return_value=settlement_entity)

        result = await settlement_service.add_settlement(settlement_request_dto)
        print(f"✅ Settlement successfully created with ID: {result.id}")

        assert isinstance(result, SettlementReponseDTO)
        assert result.id == settlement_entity.id
        assert result.nombre == settlement_entity.nombre
        settlement_repository.exists_by.assert_called_once_with(
            nombre=settlement_request_dto.nombre
        )
        settlement_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_settlement_conflict(
        self, settlement_service, settlement_repository, settlement_request_dto
    ):
        """
        Tests settlement creation with a name that already exists.
        """
        print(
            f"\n🔹 Attempting to create duplicate settlement: '{settlement_request_dto.nombre}' 🔹"
        )
        settlement_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await settlement_service.add_settlement(settlement_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert (
            f"Settlement with name {settlement_request_dto.nombre} already exists"
            in str(exc_info.value)
        )
        settlement_repository.exists_by.assert_called_once_with(
            nombre=settlement_request_dto.nombre
        )
        settlement_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_settlements(
        self, settlement_service, settlement_repository, settlement_entity
    ):
        """
        Tests retrieving all settlements.
        """
        print("\n🔹 Getting all settlements 🔍")
        settlements = [
            settlement_entity,
            CentroPoblado(id=2, nombre="Miraflores", created_at=datetime.now()),
        ]
        settlement_repository.get_all = AsyncMock(return_value=settlements)

        result = await settlement_service.get_all_settlements()
        print(f"📋 Found {len(result)} settlements")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(
            isinstance(settlement, SettlementReponseDTO) for settlement in result
        )
        assert result[0].id == 1
        assert result[0].nombre == "San Isidro"
        assert result[1].id == 2
        assert result[1].nombre == "Miraflores"
        settlement_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_settlement_success(
        self, settlement_service, settlement_repository, settlement_entity
    ):
        """
        Tests successful settlement update.
        """
        print(f"\n🔹 Updating settlement ID: 1 to name: 'San Isidro Labrador' 🔄")
        updated_request = SettlementRequestDTO(nombre="San Isidro Labrador")
        updated_entity = CentroPoblado(
            id=1,
            nombre="San Isidro Labrador",
            created_at=settlement_entity.created_at,
            updated_at=datetime.now(),
        )

        settlement_repository.exists_by = AsyncMock(side_effect=[True, False])
        settlement_repository.get_by_id = AsyncMock(return_value=settlement_entity)
        settlement_repository.save = AsyncMock(return_value=updated_entity)

        result = await settlement_service.update_settlement(1, updated_request)
        print(f"✅ Settlement successfully updated: {result.nombre}")

        assert isinstance(result, SettlementReponseDTO)
        assert result.id == 1
        assert result.nombre == "San Isidro Labrador"
        assert result.updated_at is not None
        settlement_repository.exists_by.assert_any_call(id=1)
        settlement_repository.exists_by.assert_any_call(nombre="San Isidro Labrador")
        settlement_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_settlement_not_found(
        self, settlement_service, settlement_repository
    ):
        """
        Tests settlement update when the settlement doesn't exist.
        """
        print(f"\n🔹 Attempting to update non-existent settlement (ID: 999) 🔄")
        updated_request = SettlementRequestDTO(nombre="San Isidro Labrador")
        settlement_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await settlement_service.update_settlement(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Settlement with id 999 not found" in str(exc_info.value)
        settlement_repository.exists_by.assert_called_once_with(id=999)
        settlement_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_settlement_name_conflict(
        self, settlement_service, settlement_repository, settlement_entity
    ):
        """
        Tests settlement update with a conflicting name.
        """
        print(f"\n🔹 Attempting to update to an existing name: 'Miraflores' 🔄")
        updated_request = SettlementRequestDTO(nombre="Miraflores")
        settlement_repository.exists_by = AsyncMock(side_effect=[True, True])
        settlement_repository.get_by_id = AsyncMock(return_value=settlement_entity)

        with pytest.raises(ConflictException) as exc_info:
            await settlement_service.update_settlement(1, updated_request)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert "Settlement with name Miraflores already exists" in str(exc_info.value)
        settlement_repository.exists_by.assert_any_call(id=1)
        settlement_repository.exists_by.assert_any_call(nombre="Miraflores")
        settlement_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_settlement_success(
        self, settlement_service, settlement_repository
    ):
        """
        Tests successful settlement deletion.
        """
        print("\n🔹 Deleting settlement (ID: 1) 🗑️")
        settlement_repository.exists_by = AsyncMock(return_value=True)
        settlement_repository.delete = AsyncMock(return_value=True)

        result = await settlement_service.delete_settlement(1)
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Settlement deleted successfully" in result.message
        settlement_repository.exists_by.assert_called_once_with(id=1)
        settlement_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_settlement_not_found(
        self, settlement_service, settlement_repository
    ):
        """
        Tests settlement deletion when the settlement doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent settlement (ID: 999) 🗑️")
        settlement_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await settlement_service.delete_settlement(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Settlement with id 999 not found" in str(exc_info.value)
        settlement_repository.exists_by.assert_called_once_with(id=999)
        settlement_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_settlement_failure(
        self, settlement_service, settlement_repository
    ):
        """
        Tests settlement deletion when the repository operation fails.
        """
        print("\n🔹 Simulating failure in settlement deletion (ID: 1) 🗑️")
        settlement_repository.exists_by = AsyncMock(return_value=True)
        settlement_repository.delete = AsyncMock(return_value=False)

        result = await settlement_service.delete_settlement(1)
        print(f"⚠️ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete settlement" in result.message
        settlement_repository.exists_by.assert_called_once_with(id=1)
        settlement_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_settlement_by_id_success(
        self, settlement_service, settlement_repository, settlement_entity
    ):
        """
        Tests retrieving a settlement by ID.
        """
        print("\n🔹 Finding settlement by ID: 1 🔍")
        settlement_repository.exists_by = AsyncMock(return_value=True)
        settlement_repository.get_by_id = AsyncMock(return_value=settlement_entity)

        result = await settlement_service.get_settlement_by_id(1)
        print(f"✅ Settlement found: '{result.nombre}'")

        assert isinstance(result, SettlementReponseDTO)
        assert result.id == 1
        assert result.nombre == "San Isidro"
        settlement_repository.exists_by.assert_called_once_with(id=1)
        settlement_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_settlement_by_id_not_found(
        self, settlement_service, settlement_repository
    ):
        """
        Tests retrieving a non-existent settlement by ID.
        """
        print("\n🔹 Finding non-existent settlement by ID: 999 🔍")
        settlement_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await settlement_service.get_settlement_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Settlement with id 999 not found" in str(exc_info.value)
        settlement_repository.exists_by.assert_called_once_with(id=999)
        settlement_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_settlements_paginated_success(
        self, settlement_service, settlement_repository, settlement_entity
    ):
        """
        Tests retrieving paginated settlements.
        """
        print("\n🔹 Getting settlements with pagination (page: 1, size: 10) 📄")
        settlements = [
            settlement_entity,
            CentroPoblado(id=2, nombre="Miraflores", created_at=datetime.now()),
        ]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=settlements, meta=pagination)

        settlement_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await settlement_service.get_settlements_paginated(page=1, size=10)
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} in total"
        )

        assert isinstance(result, SettlementPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        settlement_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_get_settlements_paginated_invalid_params(self, settlement_service):
        """
        Tests retrieving paginated settlements with invalid parameters.
        """
        print("\n🔹 Testing pagination with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await settlement_service.get_settlements_paginated(page=0, size=10)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await settlement_service.get_settlements_paginated(page=1, size=0)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_success(
        self, settlement_service, settlement_repository, settlement_entity
    ):
        """
        Tests searching for settlements with filter criteria.
        """
        print("\n🔹 Searching for settlements containing 'San' 🔍")
        settlements = [settlement_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=settlements, meta=pagination)

        settlement_repository.find = AsyncMock(return_value=page_result)

        result = await settlement_service.find(page=1, size=10, search_term="San")
        print(f"🔎 Found {len(result.data)} settlements with 'San'")
        for item in result.data:
            print(f"  - {item.nombre} (ID: {item.id})")

        assert isinstance(result, SettlementPage)
        assert len(result.data) == 1
        assert result.data[0].nombre == "San Isidro"
        assert result.meta.total == 1
        settlement_repository.find.assert_called_once_with(1, 10, {"nombre": "San"})

    @pytest.mark.asyncio
    async def test_find_invalid_params(self, settlement_service):
        """
        Tests searching for settlements with invalid parameters.
        """
        print("\n🔹 Testing search with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await settlement_service.find(page=0, size=10, search_term="San")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await settlement_service.find(page=1, size=0, search_term="San")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_not_found(self, settlement_service, settlement_repository):
        """
        Tests searching for settlements when none are found.
        """
        print("\n🔹 Searching for non-existent settlement term: 'NotFound' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=[], meta=pagination)
        settlement_repository.find = AsyncMock(return_value=page_result)

        with pytest.raises(NotFoundException) as exc_info:
            await settlement_service.find(page=1, size=10, search_term="NotFound")
        print(f"⚠️ Expected error: {exc_info.value}")

        assert "No settlements found with the search term NotFound" in str(
            exc_info.value
        )
        settlement_repository.find.assert_called_once_with(
            1, 10, {"nombre": "NotFound"}
        )
