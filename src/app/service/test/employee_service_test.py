import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Employee
from src.app.dto.request import EmployeeRequestDTO
from src.app.dto.response import EmployeeResponseDTO, EmployeePage
from src.app.service.implementations import EmployeeServiceImpl
from src.app.core.exception import (
    ConflictException,
    NotFoundException,
    BadRequestException,
)
from src.app.core.schema import Page, Pagination, MessageResponse
from src.app.model.enum.gender_enum import GeneroEnum


class TestEmployeeServiceImpl:
    @pytest.fixture
    def employee_repository(self):
        """
        Creates a mock repository for testing the employee service.

        Returns:
            A mock employee repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def position_repository(self):
        """
        Creates a mock position repository for testing the employee service.

        Returns:
            A mock position repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def area_repository(self):
        """
        Creates a mock area repository for testing the employee service.

        Returns:
            A mock area repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def employee_service(
        self, employee_repository, position_repository, area_repository
    ):
        """
        Creates an employee service instance for testing.

        Args:
            employee_repository: The mock employee repository to inject.
            position_repository: The mock position repository to inject.
            area_repository: The mock area repository to inject.

        Returns:
            An instance of EmployeeServiceImpl with the mock repositories.
        """
        return EmployeeServiceImpl(
            repository=employee_repository,
            position_repository=position_repository,
            area_repository=area_repository,
        )

    @pytest.fixture
    def employee_request_dto(self):
        """
        Creates a sample employee request DTO.

        Returns:
            An EmployeeRequestDto instance with test data.
        """
        return EmployeeRequestDTO(
            dni=12345678,
            nombres="John",
            apellido_paterno="Doe",
            apellido_materno="Smith",
            genero=GeneroEnum.MALE,
            cargo_id=1,
            area_id=1,
        )

    @pytest.fixture
    def employee_entity(self):
        """
        Creates a sample employee entity.

        Returns:
            A Trabajador instance with test data.
        """
        return Employee(
            id=1,
            dni=12345678,
            nombres="John",
            apellido_paterno="Doe",
            apellido_materno="Smith",
            genero=GeneroEnum.MALE.value,
            cargo_id=1,
            area_id=1,
            created_at=datetime.now(),
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_add_employee_success(
        self,
        employee_service,
        employee_repository,
        position_repository,
        area_repository,
        employee_request_dto,
        employee_entity,
    ):
        """
        Tests successful employee creation.
        """
        print(
            f"\n🔹 Creating new employee: '{employee_request_dto.nombres} {employee_request_dto.apellido_paterno}' 🔹"
        )

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=False)
        position_repository.exists_by = AsyncMock(return_value=True)
        area_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.save = AsyncMock(return_value=employee_entity)

        # Execute test
        result = await employee_service.add_employee(employee_request_dto)
        print(f"✅ Employee successfully created with ID: {result.id}")

        # Verify results
        assert isinstance(result, EmployeeResponseDTO)
        assert result.id == employee_entity.id
        assert result.dni == employee_entity.dni
        assert result.nombres == employee_entity.nombres
        assert result.apellido_paterno == employee_entity.apellido_paterno

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(
            dni=employee_request_dto.dni
        )
        position_repository.exists_by.assert_called_once_with(
            id=employee_request_dto.cargo_id
        )
        area_repository.exists_by.assert_called_once_with(
            id=employee_request_dto.area_id
        )
        employee_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_employee_dni_conflict(
        self, employee_service, employee_repository, employee_request_dto
    ):
        """
        Tests employee creation with a DNI that already exists.
        """
        print(
            f"\n🔹 Attempting to create employee with existing DNI: '{employee_request_dto.dni}' 🔹"
        )

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=True)

        # Execute test and verify exception
        with pytest.raises(ConflictException) as exc_info:
            await employee_service.add_employee(employee_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        # Verify the exception message
        assert f"Employee with DNI {employee_request_dto.dni} already exists" in str(
            exc_info.value
        )

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(
            dni=employee_request_dto.dni
        )
        employee_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_employee_position_not_found(
        self,
        employee_service,
        employee_repository,
        position_repository,
        employee_request_dto,
    ):
        """
        Tests employee creation with a non-existent position ID.
        """
        print(
            f"\n🔹 Attempting to create employee with non-existent position ID: {employee_request_dto.cargo_id} 🔹"
        )

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=False)
        position_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await employee_service.add_employee(employee_request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert (
            f"Position with ID {employee_request_dto.cargo_id} does not exist"
            in str(exc_info.value)
        )

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(
            dni=employee_request_dto.dni
        )
        position_repository.exists_by.assert_called_once_with(
            id=employee_request_dto.cargo_id
        )
        employee_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_employee_area_not_found(
        self,
        employee_service,
        employee_repository,
        position_repository,
        area_repository,
        employee_request_dto,
    ):
        """
        Tests employee creation with a non-existent area ID.
        """
        print(
            f"\n🔹 Attempting to create employee with non-existent area ID: {employee_request_dto.area_id} 🔹"
        )

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=False)
        position_repository.exists_by = AsyncMock(return_value=True)
        area_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await employee_service.add_employee(employee_request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert f"Area with ID {employee_request_dto.area_id} does not exist" in str(
            exc_info.value
        )

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(
            dni=employee_request_dto.dni
        )
        position_repository.exists_by.assert_called_once_with(
            id=employee_request_dto.cargo_id
        )
        area_repository.exists_by.assert_called_once_with(
            id=employee_request_dto.area_id
        )
        employee_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_employees(
        self, employee_service, employee_repository, employee_entity
    ):
        """
        Tests retrieving all employees.
        """
        print("\n🔹 Getting all employees 🔍")

        # Create test data
        employees = [
            employee_entity,
            Employee(
                id=2,
                dni="87654321",
                nombres="Jane",
                apellido_paterno="Smith",
                apellido_materno="Doe",
                genero=GeneroEnum.FEMALE.value,
                cargo_id=2,
                area_id=2,
                created_at=datetime.now(),
                updated_at=None,
            ),
        ]

        # Configure mocks
        employee_repository.get_all = AsyncMock(return_value=employees)

        # Execute test
        result = await employee_service.get_all_employees()
        print(f"📋 Found {len(result)} employees")

        # Verify results
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(employee, EmployeeResponseDTO) for employee in result)
        assert result[0].id == 1
        assert result[0].nombres == "John"
        assert result[1].id == 2
        assert result[1].nombres == "Jane"

        # Verify method calls
        employee_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_employee_success(
        self,
        employee_service,
        employee_repository,
        position_repository,
        area_repository,
        employee_entity,
    ):
        """
        Tests successful employee update.
        """
        print(f"\n🔹 Updating employee ID: 1 🔄")

        # Create updated request
        updated_request = EmployeeRequestDTO(
            dni="12345678",
            nombres="John Updated",
            apellido_paterno="Doe Updated",
            apellido_materno="Smith Updated",
            genero=GeneroEnum.MALE,
            cargo_id=1,
            area_id=1,
        )

        # Create updated entity
        updated_entity = Employee(
            id=1,
            dni="12345678",
            nombres="John Updated",
            apellido_paterno="Doe Updated",
            apellido_materno="Smith Updated",
            genero=GeneroEnum.MALE.value,
            cargo_id=1,
            area_id=1,
            created_at=employee_entity.created_at,
            updated_at=datetime.now(),
        )

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.get_by_id = AsyncMock(return_value=employee_entity)
        position_repository.exists_by = AsyncMock(return_value=True)
        area_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.save = AsyncMock(return_value=updated_entity)

        # Execute test
        result = await employee_service.update_employee(1, updated_request)
        print(
            f"✅ Employee successfully updated: {result.nombres} {result.apellido_paterno}"
        )

        # Verify results
        assert isinstance(result, EmployeeResponseDTO)
        assert result.id == 1
        assert result.nombres == "John Updated"
        assert result.apellido_paterno == "Doe Updated"
        assert result.updated_at is not None

        # Verify method calls
        employee_repository.exists_by.assert_called_with(id=1)
        employee_repository.get_by_id.assert_called_once_with(1)
        position_repository.exists_by.assert_called_once_with(
            id=updated_request.cargo_id
        )
        area_repository.exists_by.assert_called_once_with(id=updated_request.area_id)
        employee_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_employee_not_found(
        self, employee_service, employee_repository
    ):
        """
        Tests employee update when the employee doesn't exist.
        """
        print(f"\n🔹 Attempting to update non-existent employee (ID: 999) 🔄")

        # Create update request
        updated_request = EmployeeRequestDTO(
            dni="12345678",
            nombres="John Updated",
            apellido_paterno="Doe Updated",
            apellido_materno="Smith Updated",
            genero=GeneroEnum.MALE,
            cargo_id=1,
            area_id=1,
        )

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await employee_service.update_employee(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Employee with id 999 not found" in str(exc_info.value)

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(id=999)
        employee_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_employee_dni_conflict(
        self, employee_service, employee_repository, employee_entity
    ):
        """
        Tests employee update with a conflicting DNI.
        """
        print(f"\n🔹 Attempting to update employee to a DNI already in use 🔄")

        # Create update request with new DNI
        updated_request = EmployeeRequestDTO(
            dni="87654321",  # Different from current DNI
            nombres="John Updated",
            apellido_paterno="Doe Updated",
            apellido_materno="Smith Updated",
            genero=GeneroEnum.MALE,
            cargo_id=1,
            area_id=1,
        )

        # Configure mocks
        employee_repository.exists_by = AsyncMock(
            side_effect=[True, True]
        )  # ID exists, DNI exists
        employee_repository.get_by_id = AsyncMock(return_value=employee_entity)

        # Execute test and verify exception
        with pytest.raises(ConflictException) as exc_info:
            await employee_service.update_employee(1, updated_request)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        # Verify the exception message
        assert f"Employee with DNI {updated_request.dni} already exists" in str(
            exc_info.value
        )

        # Verify method calls
        employee_repository.exists_by.assert_any_call(id=1)
        employee_repository.exists_by.assert_any_call(dni=updated_request.dni)
        employee_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_employee_success(self, employee_service, employee_repository):
        """
        Tests successful employee deletion.
        """
        print("\n🔹 Deleting employee (ID: 1) 🗑️")

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.delete = AsyncMock(return_value=True)

        # Execute test
        result = await employee_service.delete_employee(1)
        print(f"✅ {result.detail}")

        # Verify results
        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Employee deleted successfully" in result.message

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(id=1)
        employee_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_employee_not_found(
        self, employee_service, employee_repository
    ):
        """
        Tests employee deletion when the employee doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent employee (ID: 999) 🗑️")

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await employee_service.delete_employee(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Employee with id 999 not found" in str(exc_info.value)

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(id=999)
        employee_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_employee_by_id_success(
        self, employee_service, employee_repository, employee_entity
    ):
        """
        Tests retrieving an employee by ID.
        """
        print("\n🔹 Finding employee by ID: 1 🔍")

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.get_by_id = AsyncMock(return_value=employee_entity)

        # Execute test
        result = await employee_service.get_employee_by_id(1)
        print(f"✅ Employee found: '{result.nombres} {result.apellido_paterno}'")

        # Verify results
        assert isinstance(result, EmployeeResponseDTO)
        assert result.id == 1
        assert result.nombres == "John"
        assert result.apellido_paterno == "Doe"

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(id=1)
        employee_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_employee_by_id_not_found(
        self, employee_service, employee_repository
    ):
        """
        Tests retrieving a non-existent employee by ID.
        """
        print("\n🔹 Finding non-existent employee by ID: 999 🔍")

        # Configure mocks
        employee_repository.exists_by = AsyncMock(return_value=False)

        # Execute test and verify exception
        with pytest.raises(NotFoundException) as exc_info:
            await employee_service.get_employee_by_id(999)
        print(f"⚠️ Error: {exc_info.value}")

        # Verify the exception message
        assert "Employee with id 999 not found" in str(exc_info.value)

        # Verify method calls
        employee_repository.exists_by.assert_called_once_with(id=999)
        employee_repository.get_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_employees_paginated_success(
        self, employee_service, employee_repository, employee_entity
    ):
        """
        Tests retrieving paginated employees.
        """
        print("\n🔹 Getting employees with pagination (page: 1, size: 10) 📄")

        employees_data = [
            {
                "id": 1,
                "dni": "12345678",
                "nombres": "John",
                "apellido_paterno": "Doe",
                "apellido_materno": "Smith",
                "genero": "Masculino",
                "area_id": 1,
                "cargo_id": 1,
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "dni": "87654321",
                "nombres": "Jane",
                "apellido_paterno": "Smith",
                "apellido_materno": "Doe",
                "genero": "Femenino",
                "area_id": 2,
                "cargo_id": 2,
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
        page_result = Page(data=employees_data, meta=pagination)

        employee_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await employee_service.get_employees_paginated(page=1, size=10)
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} in total"
        )

        assert isinstance(result, EmployeePage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1

        employee_repository.get_pageable.assert_called_once_with(1, 10)

    @pytest.mark.asyncio
    async def test_get_employees_paginated_invalid_params(self, employee_service):
        """
        Tests retrieving paginated employees with invalid parameters.
        """
        print("\n🔹 Testing pagination with invalid parameters ⚠️")

        # Test invalid page number
        print("  - Testing with page = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await employee_service.get_employees_paginated(page=0, size=10)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Page number must be greater than 0" in str(exc_info.value)

        # Test invalid size number
        print("  - Testing with size = 0")
        with pytest.raises(BadRequestException) as exc_info:
            await employee_service.get_employees_paginated(page=1, size=0)
        print(f"  ❌ Error correctly validated: {exc_info.value}")
        assert "Size number must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_success(
        self, employee_service, employee_repository, employee_entity
    ):
        """
        Tests searching for employees with filter criteria.
        """
        print("\n🔹 Searching for employees with search criteria 🔍")

        employees_data = [
            {
                "id": 1,
                "dni": "12345678",
                "nombres": "John",
                "apellido_paterno": "Doe",
                "apellido_materno": "Smith",
                "genero": "Masculino",
                "area_id": 1,
                "cargo_id": 1,
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
        page_result = Page(data=employees_data, meta=pagination)

        employee_repository.find = AsyncMock(return_value=page_result)

        search_term = "John"

        result = await employee_service.find(page=1, size=10, search_term=search_term)
        print(f"🔎 Found {len(result.data)} employees matching search criteria")

        assert isinstance(result, EmployeePage)
        assert len(result.data) == 1
        assert result.data[0].nombres == "John"
        assert result.meta.total == 1

        employee_repository.find.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_not_found(self, employee_service, employee_repository):
        """
        Tests searching for employees when none are found.
        """
        print("\n🔹 Searching for non-existent employees 🔍")

        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=[], meta=pagination)

        employee_repository.find = AsyncMock(return_value=page_result)

        search_term = "NotFound"

        with pytest.raises(NotFoundException) as exc_info:
            await employee_service.find(page=1, size=10, search_term=search_term)
        print(f"⚠️ Expected error: {exc_info.value}")

        assert "No employees found with the provided search criteria" in str(
            exc_info.value
        )

        employee_repository.find.assert_called_once()
