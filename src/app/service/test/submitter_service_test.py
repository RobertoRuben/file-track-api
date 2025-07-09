import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Submitter
from src.app.dto.request import SubmitterRequestDTO
from src.app.dto.response import SubmitterResponseDTO, SubmitterPage
from src.app.service.implementations import SubmitterServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse
from src.app.model.enum import GeneroEnum


class TestSubmitterServiceImpl:
    @pytest.fixture
    def submitter_repository(self):
        """
        Creates a mock repository for testing the submitter service.

        :return: A mock of the submitter repository with predefined asynchronous methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def submitter_service(self, submitter_repository):
        """
        Creates an instance of the submitter service for testing.

        :param submitter_repository: The mock repository to inject
        :return: An instance of SubmitterServiceImpl with the mock repository
        """
        return SubmitterServiceImpl(submitter_repository=submitter_repository)

    @pytest.fixture
    def submitter_request_dto(self):
        """
        Creates a sample submitter request DTO.

        :return: An instance of SubmitterRequestDTO with test data
        """
        return SubmitterRequestDTO(
            dni="12345678",
            names="Juan",
            paternal_surname="Pérez",
            maternal_surname="García",
            gender=GeneroEnum.MALE,
        )

    @pytest.fixture
    def submitter_entity(self):
        """
        Creates a sample submitter entity.

        :return: An instance of Submitter with test data
        """
        return Submitter(
            id=1,
            dni=12345678,  # Must be a number, not a string
            names="Juan",
            paternal_surname="Pérez",
            maternal_surname="García",
            gender="Masculino",  # Must match the allowed values in the check constraint
            created_at=datetime(2025, 3, 24, 14, 36, 59, 588144),
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_add_submitter_success(
        self,
        submitter_service,
        submitter_repository,
        submitter_request_dto,
        submitter_entity,
    ):
        """
        Tests the successful creation of a submitter.
        """
        print(
            f"\n🔹 Creating new submitter: '{submitter_request_dto.names} {submitter_request_dto.paternal_surname}' 🔹"
        )
        submitter_repository.exists_by = AsyncMock(return_value=False)
        submitter_repository.save = AsyncMock(return_value=submitter_entity)

        result = await submitter_service.add_submitter(submitter_request_dto)
        print(f"✅ Submitter successfully created with ID: {result.id}")

        assert isinstance(result, SubmitterResponseDTO)
        assert result.id == submitter_entity.id
        assert result.dni == submitter_entity.dni
        assert result.names == submitter_entity.names
        assert result.paternal_surname == submitter_entity.paternal_surname
        assert result.maternal_surname == submitter_entity.maternal_surname
        assert result.gender == submitter_entity.gender
        submitter_repository.exists_by.assert_called_once_with(
            dni=submitter_request_dto.dni
        )
        submitter_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_submitter_conflict(
        self, submitter_service, submitter_repository, submitter_request_dto
    ):
        """
        Tests the creation of a submitter with a DNI that already exists.
        """
        print(
            f"\n🔹 Attempting to create a duplicate submitter with DNI: '{submitter_request_dto.dni}' 🔹"
        )
        submitter_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await submitter_service.add_submitter(submitter_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert f"Submitter with DNI {submitter_request_dto.dni} already exists" in str(
            exc_info.value
        )
        submitter_repository.exists_by.assert_called_once_with(
            dni=submitter_request_dto.dni
        )
        submitter_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_submitters(
        self, submitter_service, submitter_repository, submitter_entity
    ):
        """
        Tests retrieving all submitters.
        """
        print("\n🔹 Getting all submitters 🔍")
        submitters = [
            submitter_entity,
            Submitter(
                id=2,
                dni=87654321,
                names="María",
                paternal_surname="López",
                maternal_surname="Rodríguez",
                gender="Femenino",  # Allowed value according to constraint
                created_at=datetime.now(),
            ),
        ]
        submitter_repository.get_all = AsyncMock(return_value=submitters)

        result = await submitter_service.get_all_submitters()
        print(f"📋 Found {len(result)} submitters")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(submitter, SubmitterResponseDTO) for submitter in result)
        assert result[0].id == 1
        assert result[0].names == "Juan"
        assert result[1].id == 2
        assert result[1].names == "María"
        submitter_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_submitter_success(
        self, submitter_service, submitter_repository, submitter_entity
    ):
        """
        Tests the successful update of a submitter.
        """
        print(f"\n🔹 Updating submitter ID: 1 to name: 'Pedro' 🔄")
        updated_request = SubmitterRequestDTO(
            dni=12345678,
            names="Pedro",
            paternal_surname="Pérez",
            maternal_surname="García",
            gender=GeneroEnum.MALE,
        )
        updated_entity = Submitter(
            id=1,
            dni=12345678,
            names="Pedro",
            paternal_surname="Pérez",
            maternal_surname="García",
            gender="Masculino",  # Allowed value according to constraint
            created_at=submitter_entity.created_at,
            updated_at=datetime.now(),
        )

        submitter_repository.exists_by = AsyncMock(side_effect=[True, False])
        submitter_repository.get_by_id = AsyncMock(return_value=submitter_entity)
        submitter_repository.save = AsyncMock(return_value=updated_entity)

        result = await submitter_service.update_submitter(1, updated_request)
        print(f"✅ Submitter successfully updated: {result.names}")

        assert isinstance(result, SubmitterResponseDTO)
        assert result.id == 1
        assert result.names == "Pedro"
        assert result.updated_at is not None
        submitter_repository.exists_by.assert_any_call(id=1)
        submitter_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_submitter_not_found(
        self, submitter_service, submitter_repository
    ):
        """
        Tests updating a submitter when it doesn't exist.
        """
        print(f"\n🔹 Attempting to update a non-existent submitter (ID: 999) 🔄")
        updated_request = SubmitterRequestDTO(
            dni=12345678,
            names="Pedro",
            paternal_surname="Pérez",
            maternal_surname="García",
            gender=GeneroEnum.MALE,
        )
        submitter_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await submitter_service.update_submitter(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Submitter with id 999 not found" in str(exc_info.value)
        submitter_repository.exists_by.assert_called_once_with(id=999)
        submitter_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_submitter_dni_conflict(
        self, submitter_service, submitter_repository, submitter_entity
    ):
        """
        Tests updating a submitter with a DNI that already exists.
        """
        print(f"\n🔹 Attempting to update to an existing DNI: '87654321' 🔄")
        updated_request = SubmitterRequestDTO(
            dni=87654321,
            names="Juan",
            paternal_surname="Pérez",
            maternal_surname="García",
            gender=GeneroEnum.MALE,
        )
        submitter_repository.exists_by = AsyncMock(side_effect=[True, True])
        submitter_repository.get_by_id = AsyncMock(return_value=submitter_entity)

        with pytest.raises(ConflictException) as exc_info:
            await submitter_service.update_submitter(1, updated_request)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert "Submitter with DNI 87654321 already exists" in str(exc_info.value)
        submitter_repository.exists_by.assert_any_call(id=1)
        submitter_repository.exists_by.assert_any_call(dni=87654321)
        submitter_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_submitter_success(
        self, submitter_service, submitter_repository
    ):
        """
        Tests the successful deletion of a submitter.
        """
        print("\n🔹 Deleting submitter (ID: 1) 🗑️")
        submitter_repository.exists_by = AsyncMock(return_value=True)
        submitter_repository.delete = AsyncMock(return_value=True)

        result = await submitter_service.delete_submitter(1)
        print(f"✅ {result.detail}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Submitter deleted successfully" in result.message
        submitter_repository.exists_by.assert_called_once_with(id=1)
        submitter_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_submitter_not_found(
        self, submitter_service, submitter_repository
    ):
        """
        Tests deleting a submitter when it doesn't exist.
        """
        print("\n🔹 Attempting to delete a non-existent submitter (ID: 999) 🗑️")
        submitter_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await submitter_service.delete_submitter(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Submitter with id 999 not found" in str(exc_info.value)
        submitter_repository.exists_by.assert_called_once_with(id=999)
        submitter_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_submitter_failure(
        self, submitter_service, submitter_repository
    ):
        """
        Tests deleting a submitter when the repository operation fails.
        """
        print("\n🔹 Simulating failure in submitter deletion (ID: 1) 🗑️")
        submitter_repository.exists_by = AsyncMock(return_value=True)
        submitter_repository.delete = AsyncMock(return_value=False)

        result = await submitter_service.delete_submitter(1)
        print(f"⚠️ {result.detail}")

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete submitter" in result.message
        submitter_repository.exists_by.assert_called_once_with(id=1)
        submitter_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_submitter_by_id_success(
        self, submitter_service, submitter_repository, submitter_entity
    ):
        """
        Tests retrieving a submitter by its ID.
        """
        print("\n🔹 Looking for submitter by ID: 1 🔍")
        submitter_repository.exists_by = AsyncMock(return_value=True)
        submitter_repository.get_by_id = AsyncMock(return_value=submitter_entity)

        result = await submitter_service.get_submitter_by_id(1)
        print(f"✅ Submitter found: '{result.names} {result.paternal_surname}'")

        assert isinstance(result, SubmitterResponseDTO)
        assert result.id == 1
        assert result.names == "Juan"
        assert result.paternal_surname == "Pérez"
        submitter_repository.exists_by.assert_called_once_with(id=1)
        submitter_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_submitter_by_id_not_found(
        self, submitter_service, submitter_repository
    ):
        """
        Tests retrieving a non-existent submitter by ID.
        """
        print("\n🔹 Looking for non-existent submitter by ID: 999 🔍")
        submitter_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await submitter_service.get_submitter_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Submitter with id 999 not found" in str(exc_info.value)
        submitter_repository.exists_by.assert_called_once_with(id=999)
        submitter_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_submitters_paginated_success(
        self, submitter_service, submitter_repository, submitter_entity
    ):
        """
        Tests paginated retrieval of submitters.
        """
        print("\n🔹 Getting submitters with pagination (page: 1, size: 10) 📄")
        submitters = [
            submitter_entity,
            Submitter(
                id=2,
                dni=87654321,
                names="María",
                paternal_surname="López",
                maternal_surname="Rodríguez",
                gender="FEMENINO",
                created_at=datetime.now(),
            ),
        ]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=submitters, meta=pagination)

        submitter_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await submitter_service.get_submitters_paginated(page=1, size=10)
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results out of {result.meta.total} total"
        )

        assert isinstance(result, SubmitterPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        submitter_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_get_submitters_paginated_invalid_params(self, submitter_service):
        """
        Tests paginated retrieval of submitters with invalid parameters.
        """
        print("\n🔹 Testing pagination with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await submitter_service.get_submitters_paginated(page=0, size=10)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await submitter_service.get_submitters_paginated(page=1, size=0)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_success(
        self, submitter_service, submitter_repository, submitter_entity
    ):
        """
        Tests searching submitters with filter criteria.
        """
        print("\n🔹 Searching for submitters containing 'Juan' 🔍")
        submitters = [submitter_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=submitters, meta=pagination)

        submitter_repository.find = AsyncMock(return_value=page_result)

        result = await submitter_service.find(page=1, size=10, search_term="Juan")
        print(f"🔎 Found {len(result.data)} submitters with 'Juan'")
        for item in result.data:
            print(f"  - {item.names} {item.paternal_surname} (ID: {item.id})")

        assert isinstance(result, SubmitterPage)
        assert len(result.data) == 1
        assert result.data[0].names == "Juan"
        assert result.meta.total == 1

        # Verify that it was called correctly with the search dictionary
        search_dict = {
            "names": "Juan",
            "paternal_surname": "Juan",
            "maternal_surname": "Juan",
            "dni": None,  # None because "Juan" is not a number
        }
        submitter_repository.find.assert_called_once()
        call_args = submitter_repository.find.call_args[0]
        assert call_args[0] == 1
        assert call_args[1] == 10
        assert "names" in call_args[2]
        assert call_args[2]["names"] == "Juan"

    @pytest.mark.asyncio
    async def test_find_with_numeric_search(
        self, submitter_service, submitter_repository, submitter_entity
    ):
        """
        Tests searching submitters with a numeric search term.
        """
        print("\n🔹 Searching for submitters with DNI '12345678' 🔍")
        submitters = [submitter_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=submitters, meta=pagination)

        submitter_repository.find = AsyncMock(return_value=page_result)

        result = await submitter_service.find(page=1, size=10, search_term="12345678")
        print(f"🔎 Found {len(result.data)} submitters with DNI '12345678'")

        assert isinstance(result, SubmitterPage)
        assert len(result.data) == 1

        # Verify that DNI was included in the search when the term is numeric
        submitter_repository.find.assert_called_once()
        call_args = submitter_repository.find.call_args[0]
        assert call_args[2]["dni"] == "12345678"

    @pytest.mark.asyncio
    async def test_find_invalid_params(self, submitter_service):
        """
        Tests searching submitters with invalid parameters.
        """
        print("\n🔹 Testing search with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await submitter_service.find(page=0, size=10, search_term="Juan")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await submitter_service.find(page=1, size=0, search_term="Juan")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_not_found(self, submitter_service, submitter_repository):
        """
        Tests searching submitters when none are found.
        """
        print("\n🔹 Searching for non-existent term: 'NoExiste' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=[], meta=pagination)
        submitter_repository.find = AsyncMock(return_value=page_result)

        with pytest.raises(NotFoundException) as exc_info:
            await submitter_service.find(page=1, size=10, search_term="NoExiste")
        print(f"⚠️ Expected error: {exc_info.value}")

        assert "No submitters found with the search term NoExiste" in str(
            exc_info.value
        )
        submitter_repository.find.assert_called_once()
