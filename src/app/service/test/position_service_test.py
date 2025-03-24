import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Cargo
from src.app.dto.request import PositionRequestDTO
from src.app.dto.response import PositionResponseDTO, PositionPage
from src.app.service.implementations import PositionServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestPositionServiceImpl:
    @pytest.fixture
    def position_repository(self):
        """
        Creates a mock repository for testing the position service.

        Returns:
            A mock position repository with predefined async methods.
        """
        return AsyncMock()

    @pytest.fixture
    def position_service(self, position_repository):
        """
        Creates a position service instance for testing.

        Args:
            position_repository: The mock repository to inject.

        Returns:
            An instance of PositionServiceImpl with the mock repository.
        """
        return PositionServiceImpl(repository=position_repository)

    @pytest.fixture
    def position_request_dto(self):
        """
        Creates a sample position request DTO.

        Returns:
            A PositionRequestDTO instance with test data.
        """
        return PositionRequestDTO(nombre="Project Manager")

    @pytest.fixture
    def position_entity(self):
        """
        Creates a sample position entity.

        Returns:
            A Cargo instance with test data.
        """
        return Cargo(
            id=1,
            nombre="Project Manager",
            created_at=datetime.now(),
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_add_position_success(
        self,
        position_service,
        position_repository,
        position_request_dto,
        position_entity,
    ):
        """
        Tests successful position creation.
        """
        print(f"\n🔹 Creating new position: '{position_request_dto.nombre}' 🔹")
        position_repository.exists_by.return_value = False
        position_repository.save.return_value = position_entity

        result = await position_service.add_position(position_request_dto)
        print(f"✅ Position successfully created with ID: {result.id}")

        assert isinstance(result, PositionResponseDTO)
        assert result.id == position_entity.id
        assert result.nombre == position_entity.nombre
        position_repository.exists_by.assert_called_once_with(
            nombre=position_request_dto.nombre
        )
        position_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_position_conflict(
        self,
        position_service,
        position_repository,
        position_request_dto,
    ):
        """
        Tests position creation with a name that already exists.
        """
        print(
            f"\n🔹 Attempting to create duplicate position: '{position_request_dto.nombre}' 🔹"
        )
        position_repository.exists_by.return_value = True

        with pytest.raises(ConflictException) as exc_info:
            await position_service.add_position(position_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert (
            f"Position with name {position_request_dto.nombre} already exists"
            in str(exc_info.value)
        )
        position_repository.exists_by.assert_called_once_with(
            nombre=position_request_dto.nombre
        )
        position_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_positions(
        self,
        position_service,
        position_repository,
        position_entity,
    ):
        """
        Tests retrieving all positions.
        """
        print("\n🔹 Getting all positions 🔍")
        positions = [
            position_entity,
            Cargo(id=2, nombre="Developer", created_at=datetime.now()),
        ]
        position_repository.get_all.return_value = positions

        result = await position_service.get_all_positions()
        print(f"📋 Found {len(result)} positions")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(position, PositionResponseDTO) for position in result)
        assert result[0].id == 1
        assert result[0].nombre == "Project Manager"
        assert result[1].id == 2
        assert result[1].nombre == "Developer"
        position_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_position_success(
        self,
        position_service,
        position_repository,
        position_entity,
    ):
        """
        Tests successful position update.
        """
        print(f"\n🔹 Updating position ID: 1 to name: 'Senior Project Manager' 🔄")
        updated_request = PositionRequestDTO(nombre="Senior Project Manager")
        updated_entity = Cargo(
            id=1,
            nombre="Senior Project Manager",
            created_at=position_entity.created_at,
            updated_at=datetime.now(),
        )

        position_repository.exists_by.side_effect = [True, False]
        position_repository.get_by_id.return_value = position_entity
        position_repository.save.return_value = updated_entity

        result = await position_service.update_position(1, updated_request)
        print(f"✅ Position successfully updated: {result.nombre}")

        assert isinstance(result, PositionResponseDTO)
        assert result.id == 1
        assert result.nombre == "Senior Project Manager"
        assert result.updated_at is not None
        position_repository.exists_by.assert_any_call(id=1)
        position_repository.exists_by.assert_any_call(nombre="Senior Project Manager")
        position_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_position_not_found(
        self, position_service, position_repository
    ):
        """
        Tests position update when the position doesn't exist.
        """
        print(f"\n🔹 Attempting to update non-existent position (ID: 999) 🔄")
        updated_request = PositionRequestDTO(nombre="Senior Project Manager")
        position_repository.exists_by.return_value = False

        with pytest.raises(NotFoundException) as exc_info:
            await position_service.update_position(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Position with id 999 not found" in str(exc_info.value)
        position_repository.exists_by.assert_called_once_with(id=999)
        position_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_position_name_conflict(
        self,
        position_service,
        position_repository,
        position_entity,
    ):
        """
        Tests position update with a conflicting name.
        """
        print(f"\n🔹 Attempting to update to an existing name: 'Developer' 🔄")
        updated_request = PositionRequestDTO(nombre="Developer")
        position_repository.exists_by.side_effect = [True, True]
        position_repository.get_by_id.return_value = position_entity

        with pytest.raises(ConflictException) as exc_info:
            await position_service.update_position(1, updated_request)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert "Position with name Developer already exists" in str(exc_info.value)
        position_repository.exists_by.assert_any_call(id=1)
        position_repository.exists_by.assert_any_call(nombre="Developer")
        position_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_position_success(self, position_service, position_repository):
        """
        Tests successful position deletion.
        """
        print("\n🔹 Deleting position (ID: 1) 🗑️")
        position_repository.exists_by.return_value = True
        position_repository.delete.return_value = True

        result = await position_service.delete_position(1)
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Position deleted successfully" in result.message
        position_repository.exists_by.assert_called_once_with(id=1)
        position_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_position_not_found(
        self, position_service, position_repository
    ):
        """
        Tests position deletion when the position doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent position (ID: 999) 🗑️")
        position_repository.exists_by.return_value = False

        with pytest.raises(NotFoundException) as exc_info:
            await position_service.delete_position(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Position with id 999 not found" in str(exc_info.value)
        position_repository.exists_by.assert_called_once_with(id=999)
        position_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_position_failure(self, position_service, position_repository):
        """
        Tests position deletion when the repository operation fails.
        """
        print("\n🔹 Simulating failure in position deletion (ID: 1) 🗑️")
        position_repository.exists_by.return_value = True
        position_repository.delete.return_value = False

        result = await position_service.delete_position(1)
        print(f"⚠️ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete position" in result.message
        position_repository.exists_by.assert_called_once_with(id=1)
        position_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_position_by_id_success(
        self,
        position_service,
        position_repository,
        position_entity,
    ):
        """
        Tests retrieving a position by ID.
        """
        print("\n🔹 Finding position by ID: 1 🔍")
        position_repository.exists_by.return_value = True
        position_repository.get_by_id.return_value = position_entity

        result = await position_service.get_position_by_id(1)
        print(f"✅ Position found: '{result.nombre}'")

        assert isinstance(result, PositionResponseDTO)
        assert result.id == 1
        assert result.nombre == "Project Manager"
        position_repository.exists_by.assert_called_once_with(id=1)
        position_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_position_by_id_not_found(
        self, position_service, position_repository
    ):
        """
        Tests retrieving a non-existent position by ID.
        """
        print("\n🔹 Finding non-existent position by ID: 999 🔍")
        position_repository.exists_by.return_value = False

        with pytest.raises(NotFoundException) as exc_info:
            await position_service.get_position_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Position with id 999 not found" in str(exc_info.value)
        position_repository.exists_by.assert_called_once_with(id=999)
        position_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_positions_paginated_success(
        self,
        position_service,
        position_repository,
        position_entity,
    ):
        """
        Tests retrieving paginated positions.
        """
        print("\n🔹 Getting positions with pagination (page: 1, size: 10) 📄")
        positions = [
            position_entity,
            Cargo(id=2, nombre="Developer", created_at=datetime.now()),
        ]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=positions, meta=pagination)

        position_repository.get_pageable.return_value = page_result

        result = await position_service.get_positions_paginated(page=1, size=10)
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} in total"
        )

        assert isinstance(result, PositionPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        position_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_get_positions_paginated_invalid_params(self, position_service):
        """
        Tests retrieving paginated positions with invalid parameters.
        """
        print("\n🔹 Testing pagination with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await position_service.get_positions_paginated(page=0, size=10)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await position_service.get_positions_paginated(page=1, size=0)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_success(
        self,
        position_service,
        position_repository,
        position_entity,
    ):
        """
        Tests searching for positions with filter criteria.
        """
        print("\n🔹 Searching for positions containing 'Project' 🔍")
        positions = [position_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=positions, meta=pagination)

        position_repository.find.return_value = page_result

        result = await position_service.find(page=1, size=10, search_term="Project")
        print(f"🔎 Found {len(result.data)} positions with 'Project'")
        for item in result.data:
            print(f"  - {item.nombre} (ID: {item.id})")

        assert isinstance(result, PositionPage)
        assert len(result.data) == 1
        assert result.data[0].nombre == "Project Manager"
        assert result.meta.total == 1
        position_repository.find.assert_called_once_with(1, 10, {"nombre": "Project"})

    @pytest.mark.asyncio
    async def test_find_invalid_params(self, position_service):
        """
        Tests searching for positions with invalid parameters.
        """
        print("\n🔹 Testing search with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await position_service.find(page=0, size=10, search_term="Project")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await position_service.find(page=1, size=0, search_term="Project")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_not_found(self, position_service, position_repository):
        """
        Tests searching for positions when none are found.
        """
        print("\n🔹 Searching for non-existent position term: 'NotFound' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=[], meta=pagination)
        position_repository.find.return_value = page_result

        with pytest.raises(NotFoundException) as exc_info:
            await position_service.find(page=1, size=10, search_term="NotFound")
        print(f"⚠️ Expected error: {exc_info.value}")

        assert "No positions found with the search term NotFound" in str(exc_info.value)
        position_repository.find.assert_called_once_with(1, 10, {"nombre": "NotFound"})
