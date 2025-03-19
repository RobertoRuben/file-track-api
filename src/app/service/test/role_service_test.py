import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Rol
from src.app.dto import RoleRequestDTO
from src.app.dto.response import RoleResponseDTO, RolePage
from src.app.service.implementations import RoleServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse


class TestRoleServiceImpl:
    @pytest.fixture
    def rol_repository(self):
        """
        Creates a mock repository for testing the role service.

        Returns:
            A mock role repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def role_service(self, rol_repository):
        """
        Creates a role service instance for testing.

        Args:
            rol_repository: The mock repository to inject.

        Returns:
            An instance of RoleServiceImpl with the mock repository.
        """
        return RoleServiceImpl(repository=rol_repository)

    @pytest.fixture
    def role_request_dto(self):
        """
        Creates a sample role request DTO.

        Returns:
            A RoleRequestDTO instance with test data.
        """
        return RoleRequestDTO(nombre="Administrador")

    @pytest.fixture
    def role_entity(self):
        """
        Creates a sample role entity.

        Returns:
            A Rol instance with test data.
        """
        return Rol(
            id=1,
            nombre="Administrador",
            created_at=datetime.now(),
            updated_at=None
        )

    @pytest.mark.asyncio
    async def test_add_role_success(self, role_service, rol_repository, role_request_dto, role_entity):
        """
        Tests successful role creation.
        """
        print("🧪 Testing successful role creation...")

        rol_repository.exists_by = AsyncMock(return_value=False)
        rol_repository.save = AsyncMock(return_value=role_entity)

        result = await role_service.add_role(role_request_dto)

        assert isinstance(result, RoleResponseDTO)
        assert result.id == role_entity.id
        assert result.nombre == role_entity.nombre
        rol_repository.exists_by.assert_called_once_with(nombre=role_request_dto.nombre)
        rol_repository.save.assert_called_once()
        print(f"✅ Role created successfully: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_add_role_conflict(self, role_service, rol_repository, role_request_dto):
        """
        Tests role creation with a name that already exists.
        """
        print("🧪 Testing role creation with existing name...")

        rol_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await role_service.add_role(role_request_dto)

        assert f"Role with name {role_request_dto.nombre} already exists" in str(exc_info.value)
        rol_repository.exists_by.assert_called_once_with(nombre=role_request_dto.nombre)
        rol_repository.save.assert_not_called()
        print(f"✅ Conflict exception correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_roles(self, role_service, rol_repository, role_entity):
        """
        Tests retrieving all roles.
        """
        print("🧪 Testing retrieval of all roles...")

        roles = [role_entity, Rol(id=2, nombre="Usuario", created_at=datetime.now())]
        rol_repository.get_all = AsyncMock(return_value=roles)

        result = await role_service.get_all_roles()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(role, RoleResponseDTO) for role in result)
        assert result[0].id == 1
        assert result[0].nombre == "Administrador"
        assert result[1].id == 2
        assert result[1].nombre == "Usuario"
        rol_repository.get_all.assert_called_once()
        print(f"✅ Retrieved {len(result)} roles successfully")

    @pytest.mark.asyncio
    async def test_update_role_success(self, role_service, rol_repository, role_entity):
        """
        Tests successful role update.
        """
        print("🧪 Testing successful role update...")

        updated_request = RoleRequestDTO(nombre="Nuevo Administrador")
        updated_entity = Rol(
            id=1,
            nombre="Nuevo Administrador",
            created_at=role_entity.created_at,
            updated_at=datetime.now()
        )

        rol_repository.exists_by = AsyncMock(side_effect=[True, False])
        rol_repository.get_by_id = AsyncMock(return_value=role_entity)
        rol_repository.save = AsyncMock(return_value=updated_entity)

        result = await role_service.update_role(1, updated_request)

        assert isinstance(result, RoleResponseDTO)
        assert result.id == 1
        assert result.nombre == "Nuevo Administrador"
        assert result.updated_at is not None
        rol_repository.exists_by.assert_any_call(id=1)
        rol_repository.exists_by.assert_any_call(nombre="Nuevo Administrador")
        rol_repository.save.assert_called_once()
        print(f"✅ Role updated successfully: ID={result.id}, New Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_update_role_not_found(self, role_service, rol_repository):
        """
        Tests role update when the role doesn't exist.
        """
        print("🧪 Testing role update when role doesn't exist...")

        updated_request = RoleRequestDTO(nombre="Nuevo Administrador")
        rol_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await role_service.update_role(999, updated_request)

        assert "Role with id 999 not found" in str(exc_info.value)
        rol_repository.exists_by.assert_called_once_with(id=999)
        rol_repository.save.assert_not_called()
        print(f"✅ NotFoundException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_update_role_name_conflict(self, role_service, rol_repository, role_entity):
        """
        Tests role update with a conflicting name.
        """
        print("🧪 Testing role update with conflicting name...")

        updated_request = RoleRequestDTO(nombre="Usuario")
        rol_repository.exists_by = AsyncMock(side_effect=[True, True])
        rol_repository.get_by_id = AsyncMock(return_value=role_entity)

        with pytest.raises(ConflictException) as exc_info:
            await role_service.update_role(1, updated_request)

        assert "Role with name Usuario already exists" in str(exc_info.value)
        rol_repository.exists_by.assert_any_call(id=1)
        rol_repository.exists_by.assert_any_call(nombre="Usuario")
        rol_repository.save.assert_not_called()
        print(f"✅ ConflictException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_delete_role_success(self, role_service, rol_repository):
        """
        Tests successful role deletion.
        """
        print("🧪 Testing successful role deletion...")

        rol_repository.exists_by = AsyncMock(return_value=True)
        rol_repository.delete = AsyncMock(return_value=True)

        result = await role_service.delete_role(1)

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Role deleted successfully" in result.message
        rol_repository.exists_by.assert_called_once_with(id=1)
        rol_repository.delete.assert_called_once_with(1)
        print(f"✅ Role deleted successfully: {result.message}")

    @pytest.mark.asyncio
    async def test_delete_role_not_found(self, role_service, rol_repository):
        """
        Tests role deletion when the role doesn't exist.
        """
        print("🧪 Testing role deletion when role doesn't exist...")

        rol_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await role_service.delete_role(999)

        assert "Role with ID 999 not found" in str(exc_info.value)
        rol_repository.exists_by.assert_called_once_with(id=999)
        rol_repository.delete.assert_not_called()
        print(f"✅ NotFoundException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_delete_role_failure(self, role_service, rol_repository):
        """
        Tests role deletion when the repository operation fails.
        """
        print("🧪 Testing role deletion when repository operation fails...")

        rol_repository.exists_by = AsyncMock(return_value=True)
        rol_repository.delete = AsyncMock(return_value=False)

        result = await role_service.delete_role(1)

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete role" in result.message
        rol_repository.exists_by.assert_called_once_with(id=1)
        rol_repository.delete.assert_called_once_with(1)
        print(f"✅ Failure response correctly returned: {result.message}")

    @pytest.mark.asyncio
    async def test_get_role_by_id_success(self, role_service, rol_repository, role_entity):
        """
        Tests retrieving a role by ID.
        """
        print("🧪 Testing retrieving a role by ID...")

        rol_repository.exists_by = AsyncMock(return_value=True)
        rol_repository.get_by_id = AsyncMock(return_value=role_entity)

        result = await role_service.get_role_by_id(1)

        assert isinstance(result, RoleResponseDTO)
        assert result.id == 1
        assert result.nombre == "Administrador"
        rol_repository.exists_by.assert_called_once_with(id=1)
        rol_repository.get_by_id.assert_called_once_with(1)
        print(f"✅ Role retrieved successfully: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_get_role_by_id_not_found(self, role_service, rol_repository):
        """
        Tests retrieving a role by ID when it doesn't exist.
        """
        print("🧪 Testing retrieving a non-existent role by ID...")

        rol_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await role_service.get_role_by_id(999)

        assert "Role with ID 999 not found" in str(exc_info.value)
        rol_repository.exists_by.assert_called_once_with(id=999)
        rol_repository.get_by_id.assert_not_called()
        print(f"✅ NotFoundException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_paginated_roles_success(self, role_service, rol_repository, role_entity):
        """
        Tests retrieving paginated roles.
        """
        print("🧪 Testing retrieving paginated roles...")

        roles = [role_entity, Rol(id=2, nombre="Usuario", created_at=datetime.now())]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=roles, meta=pagination)

        rol_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await role_service.get_paginated_roles(page=1, size=10)

        assert isinstance(result, RolePage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        rol_repository.get_pageable.assert_called_once_with(page=1, size=10)
        print(f"✅ Retrieved paginated roles successfully: {len(result.data)} roles in page {result.meta.current_page}")

    @pytest.mark.asyncio
    async def test_get_paginated_roles_invalid_params(self, role_service, rol_repository):
        """
        Tests retrieving paginated roles with invalid parameters.
        """
        print("🧪 Testing paginated roles with invalid parameters...")

        # Test invalid page
        with pytest.raises(BadRequestException) as exc_info:
            await role_service.get_paginated_roles(page=0, size=10)
        assert "Page number must be greater than 0" in str(exc_info.value)
        print(f"✅ BadRequestException correctly raised for invalid page: {exc_info.value}")

        # Test invalid size
        with pytest.raises(BadRequestException) as exc_info:
            await role_service.get_paginated_roles(page=1, size=0)
        assert "Size number must be greater than 0" in str(exc_info.value)
        print(f"✅ BadRequestException correctly raised for invalid size: {exc_info.value}")


    @pytest.mark.asyncio
    async def test_find_success(self, role_service, rol_repository, role_entity):
        """
        Tests searching for roles with filter criteria.
        """
        print("🧪 Testing search for roles with filter...")

        roles = [role_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None
        )
        page_result = Page(data=roles, meta=pagination)

        rol_repository.find = AsyncMock(return_value=page_result)

        result = await role_service.find(page=1, size=10, search_term="Admin")

        assert isinstance(result, RolePage)
        assert len(result.data) == 1
        assert result.data[0].nombre == "Administrador"
        assert result.meta.total == 1
        rol_repository.find.assert_called_once_with(1, 10, {"nombre": "Admin"})
        print(f"✅ Search found {len(result.data)} roles for term 'Admin'")