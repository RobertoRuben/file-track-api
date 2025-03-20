import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Area
from src.app.dto.request import DepartmentRequestDTO
from src.app.dto.response import DepartmentResponseDTO, DepartmentPage
from src.app.service.implementations import DepartmentServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestDepartmentServiceImpl:
    @pytest.fixture
    def area_repository(self):
        """
        Creates a mock repository for testing the department service.

        Returns:
            A mock department repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def department_service(self, area_repository):
        """
        Creates a department service instance for testing.

        Args:
            area_repository: The mock repository to inject.

        Returns:
            An instance of DepartmentServiceImpl with the mock repository.
        """
        return DepartmentServiceImpl(repository=area_repository)

    @pytest.fixture
    def department_request_dto(self):
        """
        Creates a sample department request DTO.

        Returns:
            A DepartmentRequestDTO instance with test data.
        """
        return DepartmentRequestDTO(nombre="Recursos Humanos")

    @pytest.fixture
    def department_entity(self):
        """
        Creates a sample department entity.

        Returns:
            An Area instance with test data.
        """
        return Area(
            id=1,
            nombre="Recursos Humanos",
            created_at=datetime.now(),
            updated_at=None
        )

    @pytest.mark.asyncio
    async def test_add_department_success(self, department_service, area_repository, department_request_dto, department_entity):
        """
        Tests successful department creation.
        """
        print(f"\n🔹 Creating new department: '{department_request_dto.nombre}' 🔹")
        area_repository.exists_by = AsyncMock(return_value=False)
        area_repository.save = AsyncMock(return_value=department_entity)

        result = await department_service.add_department(department_request_dto)
        print(f"✅ Department successfully created with ID: {result.id}")

        assert isinstance(result, DepartmentResponseDTO)
        assert result.id == department_entity.id
        assert result.nombre == department_entity.nombre
        area_repository.exists_by.assert_called_once_with(nombre=department_request_dto.nombre)
        area_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_department_conflict(self, department_service, area_repository, department_request_dto):
        """
        Tests department creation with a name that already exists.
        """
        print(f"\n🔹 Attempting to create duplicate department: '{department_request_dto.nombre}' 🔹")
        area_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await department_service.add_department(department_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert f"Department with name {department_request_dto.nombre} already exists" in str(exc_info.value)
        area_repository.exists_by.assert_called_once_with(nombre=department_request_dto.nombre)
        area_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_departments(self, department_service, area_repository, department_entity):
        """
        Tests retrieving all departments.
        """
        print("\n🔹 Getting all departments 🔍")
        departments = [department_entity, Area(id=2, nombre="Ventas", created_at=datetime.now())]
        area_repository.get_all = AsyncMock(return_value=departments)

        result = await department_service.get_all_departments()
        print(f"📋 Found {len(result)} departments")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(dept, DepartmentResponseDTO) for dept in result)
        assert result[0].id == 1
        assert result[0].nombre == "Recursos Humanos"
        assert result[1].id == 2
        assert result[1].nombre == "Ventas"
        area_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_department_success(self, department_service, area_repository, department_entity):
        """
        Tests successful department update.
        """
        print(f"\n🔹 Updating department ID: 1 to name: 'RRHH' 🔄")
        updated_request = DepartmentRequestDTO(nombre="RRHH")
        updated_entity = Area(
            id=1,
            nombre="RRHH",
            created_at=department_entity.created_at,
            updated_at=datetime.now()
        )

        area_repository.exists_by = AsyncMock(side_effect=[True, False])
        area_repository.get_by_id = AsyncMock(return_value=department_entity)
        area_repository.save = AsyncMock(return_value=updated_entity)

        result = await department_service.update_department(1, updated_request)
        print(f"✅ Department successfully updated: {result.nombre}")

        assert isinstance(result, DepartmentResponseDTO)
        assert result.id == 1
        assert result.nombre == "RRHH"
        assert result.updated_at is not None
        area_repository.exists_by.assert_any_call(id=1)
        area_repository.exists_by.assert_any_call(nombre="RRHH")
        area_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_department_not_found(self, department_service, area_repository):
        """
        Tests department update when the department doesn't exist.
        """
        print(f"\n🔹 Attempting to update non-existent department (ID: 999) 🔄")
        updated_request = DepartmentRequestDTO(nombre="RRHH")
        area_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await department_service.update_department(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Department with id 999 not found" in str(exc_info.value)
        area_repository.exists_by.assert_called_once_with(id=999)
        area_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_department_name_conflict(self, department_service, area_repository, department_entity):
        """
        Tests department update with a conflicting name.
        """
        print(f"\n🔹 Attempting to update to an existing name: 'Ventas' 🔄")
        updated_request = DepartmentRequestDTO(nombre="Ventas")
        area_repository.exists_by = AsyncMock(side_effect=[True, True])
        area_repository.get_by_id = AsyncMock(return_value=department_entity)

        with pytest.raises(ConflictException) as exc_info:
            await department_service.update_department(1, updated_request)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert "Department with name Ventas already exists" in str(exc_info.value)
        area_repository.exists_by.assert_any_call(id=1)
        area_repository.exists_by.assert_any_call(nombre="Ventas")
        area_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_department_success(self, department_service, area_repository):
        """
        Tests successful department deletion.
        """
        print("\n🔹 Deleting department (ID: 1) 🗑️")
        area_repository.exists_by = AsyncMock(return_value=True)
        area_repository.delete = AsyncMock(return_value=True)

        result = await department_service.delete_department(1)
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Department deleted successfully" in result.message
        area_repository.exists_by.assert_called_once_with(id=1)
        area_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_department_not_found(self, department_service, area_repository):
        """
        Tests department deletion when the department doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent department (ID: 999) 🗑️")
        area_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await department_service.delete_department(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Department with id 999 not found" in str(exc_info.value)
        area_repository.exists_by.assert_called_once_with(id=999)
        area_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_department_failure(self, department_service, area_repository):
        """
        Tests department deletion when the repository operation fails.
        """
        print("\n🔹 Simulating failure in department deletion (ID: 1) 🗑️")
        area_repository.exists_by = AsyncMock(return_value=True)
        area_repository.delete = AsyncMock(return_value=False)

        result = await department_service.delete_department(1)
        print(f"⚠️ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete department" in result.message
        area_repository.exists_by.assert_called_once_with(id=1)
        area_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_department_by_id_success(self, department_service, area_repository, department_entity):
        """
        Tests retrieving a department by ID.
        """
        print("\n🔹 Finding department by ID: 1 🔍")
        area_repository.exists_by = AsyncMock(return_value=True)
        area_repository.get_by_id = AsyncMock(return_value=department_entity)

        result = await department_service.get_department_by_id(1)
        print(f"✅ Department found: '{result.nombre}'")

        assert isinstance(result, DepartmentResponseDTO)
        assert result.id == 1
        assert result.nombre == "Recursos Humanos"
        area_repository.exists_by.assert_called_once_with(id=1)
        area_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_department_by_id_not_found(self, department_service, area_repository):
        """
        Tests retrieving a non-existent department by ID.
        """
        print("\n🔹 Finding non-existent department by ID: 999 🔍")
        area_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await department_service.get_department_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "Department with id 999 not found" in str(exc_info.value)
        area_repository.exists_by.assert_called_once_with(id=999)
        area_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_departments_paginated_success(self, department_service, area_repository, department_entity):
        """
        Tests retrieving paginated departments.
        """
        print("\n🔹 Getting departments with pagination (page: 1, size: 10) 📄")
        departments = [department_entity, Area(id=2, nombre="Ventas", created_at=datetime.now())]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=departments, meta=pagination)

        area_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await department_service.get_departments_paginated(page=1, size=10)
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} in total")

        assert isinstance(result, DepartmentPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        area_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_get_departments_paginated_invalid_params(self, department_service):
        """
        Tests retrieving paginated departments with invalid parameters.
        """
        print("\n🔹 Testing pagination with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await department_service.get_departments_paginated(page=0, size=10)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await department_service.get_departments_paginated(page=1, size=0)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_success(self, department_service, area_repository, department_entity):
        """
        Tests searching for departments with filter criteria.
        """
        print("\n🔹 Searching for departments containing 'Recursos' 🔍")
        departments = [department_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=departments, meta=pagination)

        area_repository.find = AsyncMock(return_value=page_result)

        result = await department_service.find(page=1, size=10, search_term="Recursos")
        print(f"🔎 Found {len(result.data)} departments with 'Recursos'")
        for item in result.data:
            print(f"  - {item.nombre} (ID: {item.id})")

        assert isinstance(result, DepartmentPage)
        assert len(result.data) == 1
        assert result.data[0].nombre == "Recursos Humanos"
        assert result.meta.total == 1
        area_repository.find.assert_called_once_with(1, 10, {"nombre": "Recursos"})

    @pytest.mark.asyncio
    async def test_find_invalid_params(self, department_service):
        """
        Tests searching for departments with invalid parameters.
        """
        print("\n🔹 Testing search with invalid parameters ⚠️")

        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await department_service.find(page=0, size=10, search_term="Recursos")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await department_service.find(page=1, size=0, search_term="Recursos")
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_not_found(self, department_service, area_repository):
        """
        Tests searching for departments when none are found.
        """
        print("\n🔹 Searching for non-existent department term: 'NotFound' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=[], meta=pagination)
        area_repository.find = AsyncMock(return_value=page_result)

        with pytest.raises(NotFoundException) as exc_info:
            await department_service.find(page=1, size=10, search_term="NotFound")
        print(f"⚠️ Expected error: {exc_info.value}")

        assert "No departments found with the search term NotFound" in str(exc_info.value)
        area_repository.find.assert_called_once_with(1, 10, {"nombre": "NotFound"})
