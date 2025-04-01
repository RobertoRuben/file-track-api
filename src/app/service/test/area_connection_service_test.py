import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from pydantic import ValidationError
from src.app.dto.request import AreaConnectionRequestDto
from src.app.dto.response import AreaConnectionResponseDTO, AreaConnectionPage
from src.app.service.implementations import AreaConnectionServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestAreaConnectionServiceImpl:
    @pytest.fixture
    def area_connection_repository(self):
        """
        Creates a mock repository for testing the area connection service.

        Returns:
            A mock area connection repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def area_repository(self):
        """
        Creates a mock area repository for testing the area connection service.

        Returns:
            A mock area repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def area_connection_service(self, area_connection_repository, area_repository):
        """
        Creates an area connection service instance for testing.

        Args:
            area_connection_repository: The mock area connection repository to inject.
            area_repository: The mock area repository to inject.

        Returns:
            An instance of AreaConnectionServiceImpl with the mock repositories.
        """
        return AreaConnectionServiceImpl(
            repository=area_connection_repository,
            area_repository=area_repository,
        )

    @pytest.fixture
    def area_connection_request_dto(self):
        """
        Creates a sample area connection request DTO.

        Returns:
            An AreaConnectionRequestDto instance with test data.
        """
        return AreaConnectionRequestDto(
            area_origen_id=1,
            area_destino_id=2,
        )

    @pytest.fixture
    def area_connection_entity(self):
        """
        Creates a sample area connection entity.

        Returns:
            A MagicMock instance simulating a ComunicacionArea object for testing.
        """
        comunicacion = MagicMock()
        comunicacion.id = 1
        comunicacion.area_origen_id = 1
        comunicacion.area_destino_id = 2
        comunicacion.created_at = datetime.now()
        comunicacion.updated_at = None

        # Agregar propiedades para cuando se acceda a las relaciones
        area_origen = MagicMock()
        area_origen.id = 1
        area_origen.nombre = "Área Origen"

        area_destino = MagicMock()
        area_destino.id = 2
        area_destino.nombre = "Área Destino"

        comunicacion.area_origen = area_origen
        comunicacion.area_destino = area_destino

        return comunicacion

    @pytest.mark.asyncio
    async def test_add_area_connection_success(
        self,
        area_connection_service,
        area_connection_repository,
        area_repository,
        area_connection_request_dto,
        area_connection_entity,
    ):
        """
        Tests successful area connection creation.
        """
        print(
            f"\n🔹 Creating new area connection: Origin={area_connection_request_dto.area_origen_id}, "
            f"Destination={area_connection_request_dto.area_destino_id} 🔹"
        )

        # Configure mocks to ensure areas exist before creating a connection
        # Mock the behavior for area existence checks
        area_repository.exists_by = AsyncMock(return_value=True)
        area_connection_repository.exists_by = AsyncMock(return_value=False)
        area_connection_repository.save = AsyncMock(return_value=area_connection_entity)

        # Mock saving areas if they don't already exist (just for simulation)
        area_repository.save = AsyncMock(side_effect=lambda area: area)

        # Ensure both areas exist before creating the connection
        area_origen = MagicMock()
        area_origen.id = area_connection_request_dto.area_origen_id
        area_origen.nombre = "Área Origen"

        area_destino = MagicMock()
        area_destino.id = area_connection_request_dto.area_destino_id
        area_destino.nombre = "Área Destino"

        # Simulate saving areas to the repository
        await area_repository.save(area_origen)
        await area_repository.save(area_destino)

        # Execute test for adding area connection
        result = await area_connection_service.add_area_connection(
            area_connection_request_dto
        )
        print(f"✅ Area connection successfully created with ID: {result.id}")

        # Verify results
        assert isinstance(result, AreaConnectionResponseDTO)
        assert result.id == area_connection_entity.id
        assert result.area_origen_id == area_connection_entity.area_origen_id
        assert result.area_destino_id == area_connection_entity.area_destino_id

        # Verify method calls
        area_repository.exists_by.assert_any_call(
            id=area_connection_request_dto.area_origen_id
        )
        area_repository.exists_by.assert_any_call(
            id=area_connection_request_dto.area_destino_id
        )
        area_connection_repository.save.assert_called_once()

        # Ensure areas were saved before creating the connection
        area_repository.save.assert_any_call(area_origen)
        area_repository.save.assert_any_call(area_destino)

    @pytest.mark.asyncio
    async def test_add_area_connection_same_areas(self, area_connection_service):
        """
        Tests validation that prevents creating area connections with same source and destination areas.
        """
        print(
            "\n🔹 Validating area connection with same source and destination areas 🔹"
        )

        # Verificar que el DTO rechaza correctamente valores iguales
        with pytest.raises(ValidationError) as validation_error:
            AreaConnectionRequestDto(area_origen_id=1, area_destino_id=1)

        # Verificar el mensaje de error
        error_detail = str(validation_error.value)
        print(f"✅ Validation correctly prevented equal areas: {error_detail}")
        assert "Source and destination departments cannot be the same" in error_detail

    @pytest.mark.asyncio
    async def test_add_area_connection_source_not_found(
        self, area_connection_service, area_connection_repository, area_repository
    ):
        """
        Tests area connection creation with non-existent source area.
        """
        print(
            "\n🔹 Attempting to create area connection with non-existent source area 🔹"
        )

        request_dto = AreaConnectionRequestDto(area_origen_id=999, area_destino_id=2)

        # Configure mocks
        area_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await area_connection_service.add_area_connection(request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Area with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        area_repository.exists_by.assert_called_once_with(id=999)
        area_connection_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_area_connection_destination_not_found(
        self, area_connection_service, area_connection_repository, area_repository
    ):
        """
        Tests area connection creation with non-existent destination area.
        """
        print(
            "\n🔹 Attempting to create area connection with non-existent destination area 🔹"
        )

        request_dto = AreaConnectionRequestDto(area_origen_id=1, area_destino_id=999)

        # Configure mocks
        area_repository.exists_by = AsyncMock(side_effect=[True, False])

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await area_connection_service.add_area_connection(request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Area with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        area_repository.exists_by.assert_any_call(id=1)
        area_repository.exists_by.assert_any_call(id=999)
        area_connection_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_area_connection_already_exists(
        self, area_connection_service, area_connection_repository, area_repository
    ):
        """
        Tests area connection creation when the connection already exists.
        """
        print("\n🔹 Attempting to create duplicate area connection 🔹")

        request_dto = AreaConnectionRequestDto(area_origen_id=1, area_destino_id=2)

        # Configure mocks
        area_repository.exists_by = AsyncMock(return_value=True)

        # Simplifica el mock para siempre devolver True
        area_connection_repository.exists_by = AsyncMock(return_value=True)

        # Execute test and verify exception
        with pytest.raises(ConflictException) as exc_info:
            await area_connection_service.add_area_connection(request_dto)

        print(f"⚠️ Conflict detected: {exc_info.value}")

        # Verify the exception message
        assert "Area connection already exists between area 1 and area 2" in str(
            exc_info.value
        )

        # Verify method calls
        area_connection_repository.exists_by.assert_called_once()
        area_connection_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_area_connections(
        self, area_connection_service, area_connection_repository
    ):
        """
        Tests retrieving all area connections.
        """
        print("\n🔹 Getting all area connections 🔍")

        # Create test data
        connection1 = MagicMock()
        connection1.id = 1
        connection1.area_origen_id = 1
        connection1.area_destino_id = 2
        connection1.area_origen = MagicMock(id=1, nombre="Área 1")
        connection1.area_destino = MagicMock(id=2, nombre="Área 2")
        connection1.created_at = datetime.now()
        connection1.updated_at = None

        connection2 = MagicMock()
        connection2.id = 2
        connection2.area_origen_id = 2
        connection2.area_destino_id = 3
        connection2.area_origen = MagicMock(id=2, nombre="Área 2")
        connection2.area_destino = MagicMock(id=3, nombre="Área 3")
        connection2.created_at = datetime.now()
        connection2.updated_at = None

        connections = [connection1, connection2]

        # Configure mocks
        area_connection_repository.get_all = AsyncMock(return_value=connections)

        # Execute test
        result = await area_connection_service.get_all_area_connections()
        print(f"📋 Found {len(result)} connections")

        # Verify results
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(conn, AreaConnectionResponseDTO) for conn in result)
        assert result[0].id == 1
        assert result[0].area_origen_id == 1
        assert result[1].id == 2
        assert result[1].area_origen_id == 2

        # Verify method calls
        area_connection_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_area_connection_success(
        self,
        area_connection_service,
        area_connection_repository,
        area_repository,
        area_connection_entity,
    ):
        """
        Tests successful area connection update.
        """
        print(f"\n🔹 Updating area connection ID: 1 🔄")

        # Create updated request
        updated_request = AreaConnectionRequestDto(
            area_origen_id=3,
            area_destino_id=4,
        )

        # Create updated entity
        updated_entity = MagicMock()
        updated_entity.id = 1
        updated_entity.area_origen_id = 3
        updated_entity.area_destino_id = 4
        updated_entity.created_at = area_connection_entity.created_at
        updated_entity.updated_at = datetime.now()
        updated_entity.area_origen = MagicMock(id=3, nombre="Área 3")
        updated_entity.area_destino = MagicMock(id=4, nombre="Área 4")

        # Configure mocks
        area_connection_repository.exists_by = AsyncMock(return_value=True)
        area_connection_repository.get_by_id = AsyncMock(
            return_value=area_connection_entity
        )
        area_repository.exists_by = AsyncMock(return_value=True)
        area_connection_repository.save = AsyncMock(return_value=updated_entity)

        # Execute test
        result = await area_connection_service.update_area_connection(
            1, updated_request
        )
        print(
            f"✅ Area connection successfully updated: Origin={result.area_origen_id}, Destination={result.area_destino_id}"
        )

        # Verify results
        assert isinstance(result, AreaConnectionResponseDTO)
        assert result.id == 1
        assert result.area_origen_id == 3
        assert result.area_destino_id == 4
        assert result.updated_at is not None

        # Verify method calls
        area_connection_repository.get_by_id.assert_called_once_with(
            1
        )  # Expected call to get_by_id, not exists_by
        area_repository.exists_by.assert_any_call(id=updated_request.area_origen_id)
        area_repository.exists_by.assert_any_call(id=updated_request.area_destino_id)
        area_connection_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_area_connection_not_found(
        self, area_connection_service, area_connection_repository
    ):
        """
        Tests area connection update when the connection doesn't exist.
        """
        print(f"\n🔹 Attempting to update non-existent area connection (ID: 999) 🔄")

        # Create update request
        updated_request = AreaConnectionRequestDto(
            area_origen_id=3,
            area_destino_id=4,
        )

        # Configure mocks
        area_connection_repository.get_by_id = AsyncMock(
            return_value=None
        )  # No debería existir

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await area_connection_service.update_area_connection(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify exception message
        assert "Area connection with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        area_connection_repository.get_by_id.assert_called_once_with(999)

    @pytest.mark.asyncio
    async def test_delete_area_connection_success(
        self, area_connection_service, area_connection_repository
    ):
        """
        Tests successful area connection deletion.
        """
        print("\n🔹 Deleting area connection (ID: 1) 🗑️")

        # Configure mocks
        area_connection_repository.exists_by = AsyncMock(return_value=True)
        area_connection_repository.delete = AsyncMock(return_value=True)

        # Execute test
        result = await area_connection_service.delete_area_connection(1)
        print(f"✅ {result.message}")

        # Verify results
        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Area connection deleted successfully" in result.message

        # Verify method calls
        area_connection_repository.exists_by.assert_called_once_with(id=1)
        area_connection_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_area_connection_not_found(
        self, area_connection_service, area_connection_repository
    ):
        """
        Tests area connection deletion when the connection doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent area connection (ID: 999) 🗑️")

        # Configure mocks
        area_connection_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await area_connection_service.delete_area_connection(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Area connection with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        area_connection_repository.exists_by.assert_called_once_with(id=999)
        area_connection_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_area_connection_by_id_success(
        self,
        area_connection_service,
        area_connection_repository,
        area_connection_entity,
    ):
        """
        Tests retrieving an area connection by ID.
        """
        print("\n🔹 Finding area connection by ID: 1 🔍")

        # Configure mocks
        area_connection_repository.exists_by = AsyncMock(return_value=True)
        area_connection_repository.get_by_id = AsyncMock(
            return_value=area_connection_entity
        )

        # Execute test
        result = await area_connection_service.get_area_connection_by_id(1)
        print(
            f"✅ Area connection found: Origin={result.area_origen_id}, Destination={result.area_destino_id}"
        )

        # Verify results
        assert isinstance(result, AreaConnectionResponseDTO)
        assert result.id == 1
        assert result.area_origen_id == 1
        assert result.area_destino_id == 2

        # Verify method calls
        area_connection_repository.exists_by.assert_called_once_with(id=1)
        area_connection_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_area_connection_by_id_invalid_id(self, area_connection_service):
        """
        Tests retrieving an area connection with an invalid ID.
        """
        print("\n🔹 Attempting to find area connection with invalid ID: -1 🔍")

        # Execute test and verify exception
        with pytest.raises(BadRequestException) as exc_info:
            await area_connection_service.get_area_connection_by_id(-1)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Area connection ID must be greater than or equal to 0" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_get_area_connection_by_id_not_found(
        self, area_connection_service, area_connection_repository
    ):
        """
        Tests retrieving a non-existent area connection by ID.
        """
        print("\n🔹 Finding non-existent area connection by ID: 999 🔍")

        # Configure mocks
        area_connection_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await area_connection_service.get_area_connection_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Area connection with ID 999 not found" in str(exc_info.value)

        # Verify method calls
        area_connection_repository.exists_by.assert_called_once_with(id=999)
        area_connection_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_paginated_area_connections_success(
        self, area_connection_service, area_connection_repository
    ):
        """
        Tests retrieving paginated area connections.
        """
        print("\n🔹 Getting area connections with pagination (page: 1, size: 10) 📄")

        connections_data = [
            {
                "id": 1,
                "area_origen_id": 1,
                "area_destino_id": 2,
                "area_origen_nombre": "Área 1",
                "area_destino_nombre": "Área 2",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "area_origen_id": 2,
                "area_destino_id": 3,
                "area_origen_nombre": "Área 2",
                "area_destino_nombre": "Área 3",
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

        area_connection_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await area_connection_service.get_paginated_area_connections(
            page=1, size=10
        )
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} in total"
        )

        assert isinstance(result, AreaConnectionPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1

        area_connection_repository.get_pageable.assert_called_once_with(1, 10)
