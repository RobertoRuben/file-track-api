import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Ambito
from src.app.dto.request import DocumentaryTopicRequestDTO
from src.app.dto.response import DocumentaryTopicResponseDTO, DocumentaryTopicPage
from src.app.service.implementations import DocumentaryTopicServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestDocumentaryTopicServiceImpl:
    @pytest.fixture
    def documentary_topic_repository(self):
        """
        Creates a mock repository for testing the documentary topic service.

        Returns:
            A mock documentary topic repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def documentary_topic_service(self, documentary_topic_repository):
        """
        Creates a documentary topic service instance for testing.

        Args:
            documentary_topic_repository: The mock repository to inject.

        Returns:
            An instance of DocumentaryTopicServiceImpl with the mock repository.
        """
        return DocumentaryTopicServiceImpl(repository=documentary_topic_repository)

    @pytest.fixture
    def documentary_topic_request_dto(self):
        """
        Creates a sample documentary topic request DTO.

        Returns:
            A DocumentaryTopicRequestDTO instance with test data.
        """
        return DocumentaryTopicRequestDTO(nombre="Documentos Internos")

    @pytest.fixture
    def documentary_topic_entity(self):
        """
        Creates a sample documentary topic entity.

        Returns:
            An Ambito instance with test data.
        """
        return Ambito(
            id=1,
            nombre="Documentos Internos",
            created_at=datetime.now(),
            updated_at=None
        )

    @pytest.mark.asyncio
    async def test_add_documentary_topic_success(self, documentary_topic_service, documentary_topic_repository,
                                               documentary_topic_request_dto, documentary_topic_entity):
        """
        Tests successful documentary topic creation.
        """
        print(f"\n🔹 Creating new documentary topic: '{documentary_topic_request_dto.nombre}' 🔹")
        documentary_topic_repository.exists_by = AsyncMock(return_value=False)
        documentary_topic_repository.save = AsyncMock(return_value=documentary_topic_entity)

        result = await documentary_topic_service.add_documentary_topic(documentary_topic_request_dto)
        print(f"✅ Documentary topic successfully created with ID: {result.id}")

        assert isinstance(result, DocumentaryTopicResponseDTO)
        assert result.id == documentary_topic_entity.id
        assert result.nombre == documentary_topic_entity.nombre
        documentary_topic_repository.exists_by.assert_called_once_with(nombre=documentary_topic_request_dto.nombre)
        documentary_topic_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_documentary_topic_conflict(self, documentary_topic_service, documentary_topic_repository,
                                                documentary_topic_request_dto):
        """
        Tests documentary topic creation with a name that already exists.
        """
        print(f"\n🔹 Attempting to create duplicate documentary topic: '{documentary_topic_request_dto.nombre}' 🔹")
        documentary_topic_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await documentary_topic_service.add_documentary_topic(documentary_topic_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert f"Documentary topic with name {documentary_topic_request_dto.nombre} already exists" in str(exc_info.value)
        documentary_topic_repository.exists_by.assert_called_once_with(nombre=documentary_topic_request_dto.nombre)
        documentary_topic_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_documentary_topics(self, documentary_topic_service, documentary_topic_repository,
                                            documentary_topic_entity):
        """
        Tests retrieving all documentary topics.
        """
        print("\n🔹 Getting all documentary topics 🔍")
        topics = [documentary_topic_entity, Ambito(id=2, nombre="Documentos Externos", created_at=datetime.now())]
        documentary_topic_repository.get_all = AsyncMock(return_value=topics)

        result = await documentary_topic_service.get_all_documentary_topics()
        print(f"📋 Found {len(result)} documentary topics")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(topic, DocumentaryTopicResponseDTO) for topic in result)
        assert result[0].id == 1
        assert result[0].nombre == "Documentos Internos"
        assert result[1].id == 2
        assert result[1].nombre == "Documentos Externos"
        documentary_topic_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_documentary_topic_success(self, documentary_topic_service, documentary_topic_repository,
                                                  documentary_topic_entity):
        """
        Tests successful documentary topic update.
        """
        print(f"\n🔹 Updating documentary topic ID: 1 to name: 'Documentos Corporativos' 🔄")
        updated_request = DocumentaryTopicRequestDTO(nombre="Documentos Corporativos")
        updated_entity = Ambito(
            id=1,
            nombre="Documentos Corporativos",
            created_at=documentary_topic_entity.created_at,
            updated_at=datetime.now()
        )

        documentary_topic_repository.exists_by = AsyncMock(side_effect=[True, False])
        documentary_topic_repository.get_by_id = AsyncMock(return_value=documentary_topic_entity)
        documentary_topic_repository.save = AsyncMock(return_value=updated_entity)

        result = await documentary_topic_service.update_documentary_topic(1, updated_request)
        print(f"✅ Documentary topic successfully updated: {result.nombre}")

        assert isinstance(result, DocumentaryTopicResponseDTO)
        assert result.id == 1
        assert result.nombre == "Documentos Corporativos"
        assert result.updated_at is not None
        documentary_topic_repository.exists_by.assert_any_call(id=1)
        documentary_topic_repository.exists_by.assert_any_call(nombre="Documentos Corporativos")
        documentary_topic_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_documentary_topic_not_found(self, documentary_topic_service, documentary_topic_repository):
        """
        Tests documentary topic update when the topic doesn't exist.
        """
        print(f"\n🔹 Attempting to update non-existent documentary topic (ID: 999) 🔄")
        updated_request = DocumentaryTopicRequestDTO(nombre="Documentos Corporativos")
        documentary_topic_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await documentary_topic_service.update_documentary_topic(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Documentary topic with id 999 not found" in str(exc_info.value)
        documentary_topic_repository.exists_by.assert_called_once_with(id=999)
        documentary_topic_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_documentary_topic_name_conflict(self, documentary_topic_service, documentary_topic_repository,
                                                        documentary_topic_entity):
        """
        Tests documentary topic update with a conflicting name.
        """
        print(f"\n🔹 Attempting to update to an existing name: 'Documentos Externos' 🔄")
        updated_request = DocumentaryTopicRequestDTO(nombre="Documentos Externos")
        documentary_topic_repository.exists_by = AsyncMock(side_effect=[True, True])
        documentary_topic_repository.get_by_id = AsyncMock(return_value=documentary_topic_entity)

        with pytest.raises(ConflictException) as exc_info:
            await documentary_topic_service.update_documentary_topic(1, updated_request)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert "Documentary topic with name Documentos Externos already exists" in str(exc_info.value)
        documentary_topic_repository.exists_by.assert_any_call(id=1)
        documentary_topic_repository.exists_by.assert_any_call(nombre="Documentos Externos")
        documentary_topic_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_documentary_topic_success(self, documentary_topic_service, documentary_topic_repository):
        """
        Tests successful documentary topic deletion.
        """
        print("\n🔹 Deleting documentary topic (ID: 1) 🗑️")
        documentary_topic_repository.exists_by = AsyncMock(return_value=True)
        documentary_topic_repository.delete = AsyncMock(return_value=True)

        result = await documentary_topic_service.delete_documentary_topic(1)
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Documentary topic deleted successfully" in result.message
        documentary_topic_repository.exists_by.assert_called_once_with(id=1)
        documentary_topic_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_documentary_topic_not_found(self, documentary_topic_service, documentary_topic_repository):
        """
        Tests documentary topic deletion when the topic doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent documentary topic (ID: 999) 🗑️")
        documentary_topic_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await documentary_topic_service.delete_documentary_topic(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Documentary topic with id 999 not found" in str(exc_info.value)
        documentary_topic_repository.exists_by.assert_called_once_with(id=999)
        documentary_topic_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_documentary_topic_failure(self, documentary_topic_service, documentary_topic_repository):
        """
        Tests documentary topic deletion when the repository operation fails.
        """
        print("\n🔹 Simulating failure in documentary topic deletion (ID: 1) 🗑️")
        documentary_topic_repository.exists_by = AsyncMock(return_value=True)
        documentary_topic_repository.delete = AsyncMock(return_value=False)

        result = await documentary_topic_service.delete_documentary_topic(1)
        print(f"⚠️ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete documentary topic" in result.message
        documentary_topic_repository.exists_by.assert_called_once_with(id=1)
        documentary_topic_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_documentary_topic_by_id_success(self, documentary_topic_service, documentary_topic_repository,
                                                    documentary_topic_entity):
        """
        Tests retrieving a documentary topic by ID.
        """
        print("\n🔹 Finding documentary topic by ID: 1 🔍")
        documentary_topic_repository.exists_by = AsyncMock(return_value=True)
        documentary_topic_repository.get_by_id = AsyncMock(return_value=documentary_topic_entity)

        result = await documentary_topic_service.get_documentary_topic_by_id(1)
        print(f"✅ Documentary topic found: '{result.nombre}'")

        assert isinstance(result, DocumentaryTopicResponseDTO)
        assert result.id == 1
        assert result.nombre == "Documentos Internos"
        documentary_topic_repository.exists_by.assert_called_once_with(id=1)
        documentary_topic_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_documentary_topic_by_id_not_found(self, documentary_topic_service, documentary_topic_repository):
        """
        Tests retrieving a non-existent documentary topic by ID.
        """
        print("\n🔹 Finding non-existent documentary topic by ID: 999 🔍")
        documentary_topic_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await documentary_topic_service.get_documentary_topic_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Documentary topic with id 999 not found" in str(exc_info.value)
        documentary_topic_repository.exists_by.assert_called_once_with(id=999)
        documentary_topic_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_documentary_topics_paginated_success(self, documentary_topic_service, documentary_topic_repository,
                                                          documentary_topic_entity):
        """
        Tests retrieving paginated documentary topics.
        """
        print("\n🔹 Getting documentary topics with pagination (page: 1, size: 10) 📄")
        topics = [documentary_topic_entity, Ambito(id=2, nombre="Documentos Externos", created_at=datetime.now())]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=topics, meta=pagination)

        documentary_topic_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await documentary_topic_service.get_documentary_topics_paginated(page=1, size=10)
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} in total")

        assert isinstance(result, DocumentaryTopicPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        documentary_topic_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_get_documentary_topics_paginated_invalid_params(self, documentary_topic_service):
        """
        Tests retrieving paginated documentary topics with invalid parameters.
        """
        print("\n🔹 Testing pagination with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await documentary_topic_service.get_documentary_topics_paginated(page=0, size=10)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await documentary_topic_service.get_documentary_topics_paginated(page=1, size=0)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_success(self, documentary_topic_service, documentary_topic_repository,
                                documentary_topic_entity):
        """
        Tests searching for documentary topics with filter criteria.
        """
        print("\n🔹 Searching for documentary topics containing 'Documentos' 🔍")
        topics = [documentary_topic_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=topics, meta=pagination)

        documentary_topic_repository.find = AsyncMock(return_value=page_result)

        result = await documentary_topic_service.find(page=1, size=10, search_term="Documentos")
        print(f"🔎 Found {len(result.data)} documentary topics with 'Documentos'")
        for item in result.data:
            print(f"  - {item.nombre} (ID: {item.id})")

        assert isinstance(result, DocumentaryTopicPage)
        assert len(result.data) == 1
        assert result.data[0].nombre == "Documentos Internos"
        assert result.meta.total == 1
        documentary_topic_repository.find.assert_called_once_with(1, 10, {"nombre": "Documentos"})

    @pytest.mark.asyncio
    async def test_find_invalid_params(self, documentary_topic_service):
        """
        Tests searching for documentary topics with invalid parameters.
        """
        print("\n🔹 Testing search with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await documentary_topic_service.find(page=0, size=10, search_term="Documentos")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await documentary_topic_service.find(page=1, size=0, search_term="Documentos")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_not_found(self, documentary_topic_service, documentary_topic_repository):
        """
        Tests searching for documentary topics when none are found.
        """
        print("\n🔹 Searching for non-existent documentary topic term: 'NotFound' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=[], meta=pagination)
        documentary_topic_repository.find = AsyncMock(return_value=page_result)

        with pytest.raises(NotFoundException) as exc_info:
            await documentary_topic_service.find(page=1, size=10, search_term="NotFound")
        print(f"⚠️ Expected error: {exc_info.value}")

        assert "No documentary topics found with the search term NotFound" in str(exc_info.value)
        documentary_topic_repository.find.assert_called_once_with(1, 10, {"nombre": "NotFound"})