import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import Role
from src.app.dto.request import RoleRequestDTO
from src.app.dto.response import RoleResponseDTO, RolePage
from src.app.service.implementations import RoleServiceImpl
from src.app.core.exception import (
    ConflictException,
    NotFoundException,
    BadRequestException,
)
from src.app.core.schema import Page, Pagination, MessageResponse


class TestRoleServiceImpl:
    @pytest.fixture
    def role_repository(self):
        """
        Creates a mock repository for testing the role service.

        :return: A mock role repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def role_service(self, role_repository):
        """
        Creates a role service instance for testing.

        :param role_repository: The mock repository to inject
        :return: An instance of RoleServiceImpl with the mock repository
        """
        return RoleServiceImpl(repository=role_repository)

    @pytest.fixture
    def role_request_dto(self):
        """
        Creates a sample role request DTO.

        :return: A RoleRequestDTO instance with test data
        """
        return RoleRequestDTO(name="Administrator")

    @pytest.fixture
    def role_entity(self):
        """
        Creates a sample role entity.

        :return: A Role instance with test data
        """
        return Role(
            id=1, name="Administrator", created_at=datetime.now(), updated_at=None
        )

    @pytest.mark.asyncio
    async def test_add_role_success(
        self, role_service, role_repository, role_request_dto, role_entity
    ):
        """
        Tests successful role creation.
        """
        print("🧪 Testing successful role creation...")

        role_repository.exists_by = AsyncMock(return_value=False)
        role_repository.save = AsyncMock(return_value=role_entity)

        result = await role_service.add_role(role_request_dto)

        assert isinstance(result, RoleResponseDTO)
        assert result.id == role_entity.id
        assert result.name == role_entity.name
        role_repository.exists_by.assert_called_once_with(name=role_request_dto.name)
        role_repository.save.assert_called_once()
        print(f"✅ Role created successfully: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_add_role_conflict(
        self, role_service, role_repository, role_request_dto
    ):
        """
        Tests role creation with a name that already exists.
        """
        print("🧪 Testing role creation with existing name...")

        role_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await role_service.add_role(role_request_dto)

        assert f"Role with name {role_request_dto.name} already exists" in str(
            exc_info.value
        )
        role_repository.exists_by.assert_called_once_with(name=role_request_dto.name)
        role_repository.save.assert_not_called()
        print(f"✅ Conflict exception correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_roles(self, role_service, role_repository, role_entity):
        """
        Tests retrieving all roles.
        """
        print("🧪 Testing retrieval of all roles...")

        roles = [role_entity, Role(id=2, name="User", created_at=datetime.now())]
        role_repository.get_all = AsyncMock(return_value=roles)

        result = await role_service.get_all_roles()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(role, RoleResponseDTO) for role in result)
        assert result[0].id == 1
        assert result[0].name == "Administrator"
        assert result[1].id == 2
        assert result[1].name == "User"
        role_repository.get_all.assert_called_once()
        print(f"✅ Retrieved {len(result)} roles successfully")

    @pytest.mark.asyncio
    async def test_update_role_success(
        self, role_service, role_repository, role_entity
    ):
        """
        Tests successful role update.
        """
        print("🧪 Testing successful role update...")

        updated_request = RoleRequestDTO(name="New Administrator")
        updated_entity = Role(
            id=1,
            name="New Administrator",
            created_at=role_entity.created_at,
            updated_at=datetime.now(),
        )

        role_repository.exists_by = AsyncMock(side_effect=[True, False])
        role_repository.get_by_id = AsyncMock(return_value=role_entity)
        role_repository.save = AsyncMock(return_value=updated_entity)

        result = await role_service.update_role(1, updated_request)

        assert isinstance(result, RoleResponseDTO)
        assert result.id == 1
        assert result.name == "New Administrator"
        assert result.updated_at is not None
        role_repository.exists_by.assert_any_call(id=1)
        role_repository.exists_by.assert_any_call(name="New Administrator")
        role_repository.save.assert_called_once()
        print(f"✅ Role updated successfully: ID={result.id}, New Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_update_role_not_found(self, role_service, role_repository):
        """
        Tests role update when the role doesn't exist.
        """
        print("🧪 Testing role update when role doesn't exist...")

        updated_request = RoleRequestDTO(name="New Administrator")
        role_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await role_service.update_role(999, updated_request)

        assert "Role with id 999 not found" in str(exc_info.value)
        role_repository.exists_by.assert_called_once_with(id=999)
        role_repository.save.assert_not_called()
        print(f"✅ NotFoundException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_update_role_name_conflict(
        self, role_service, role_repository, role_entity
    ):
        """
        Tests role update with a conflicting name.
        """
        print("🧪 Testing role update with conflicting name...")

        updated_request = RoleRequestDTO(name="User")
        role_repository.exists_by = AsyncMock(side_effect=[True, True])
        role_repository.get_by_id = AsyncMock(return_value=role_entity)

        with pytest.raises(ConflictException) as exc_info:
            await role_service.update_role(1, updated_request)

        assert "Role with name User already exists" in str(exc_info.value)
        role_repository.exists_by.assert_any_call(id=1)
        role_repository.exists_by.assert_any_call(name="User")
        role_repository.save.assert_not_called()
        print(f"✅ ConflictException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_delete_role_success(self, role_service, role_repository):
        """
        Tests successful role deletion.
        """
        print("🧪 Testing successful role deletion...")

        role_repository.exists_by = AsyncMock(return_value=True)
        role_repository.delete = AsyncMock(return_value=True)

        result = await role_service.delete_role(1)

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Role deleted successfully" in result.message
        role_repository.exists_by.assert_called_once_with(id=1)
        role_repository.delete.assert_called_once_with(1)
        print(f"✅ Role deleted successfully: {result.message}")

    @pytest.mark.asyncio
    async def test_delete_role_not_found(self, role_service, role_repository):
        """
        Tests role deletion when the role doesn't exist.
        """
        print("🧪 Testing role deletion when role doesn't exist...")

        role_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await role_service.delete_role(999)

        assert "Role with ID 999 not found" in str(exc_info.value)
        role_repository.exists_by.assert_called_once_with(id=999)
        role_repository.delete.assert_not_called()
        print(f"✅ NotFoundException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_delete_role_failure(self, role_service, role_repository):
        """
        Tests role deletion when the repository operation fails.
        """
        print("🧪 Testing role deletion when repository operation fails...")

        role_repository.exists_by = AsyncMock(return_value=True)
        role_repository.delete = AsyncMock(return_value=False)

        result = await role_service.delete_role(1)

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete role" in result.message
        role_repository.exists_by.assert_called_once_with(id=1)
        role_repository.delete.assert_called_once_with(1)
        print(f"✅ Failure response correctly returned: {result.message}")

    @pytest.mark.asyncio
    async def test_get_role_by_id_success(
        self, role_service, role_repository, role_entity
    ):
        """
        Tests retrieving a role by ID.
        """
        print("🧪 Testing retrieving a role by ID...")

        role_repository.exists_by = AsyncMock(return_value=True)
        role_repository.get_by_id = AsyncMock(return_value=role_entity)

        result = await role_service.get_role_by_id(1)

        assert isinstance(result, RoleResponseDTO)
        assert result.id == 1
        assert result.name == "Administrator"
        role_repository.exists_by.assert_called_once_with(id=1)
        role_repository.get_by_id.assert_called_once_with(1)
        print(f"✅ Role retrieved successfully: ID={result.id}, Name='{result.name}'")

    @pytest.mark.asyncio
    async def test_get_role_by_id_not_found(self, role_service, role_repository):
        """
        Tests retrieving a role by ID when it doesn't exist.
        """
        print("🧪 Testing retrieving a non-existent role by ID...")

        role_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await role_service.get_role_by_id(999)

        assert "Role with ID 999 not found" in str(exc_info.value)
        role_repository.exists_by.assert_called_once_with(id=999)
        role_repository.get_by_id.assert_not_called()
        print(f"✅ NotFoundException correctly raised: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_paginated_roles_success(
        self, role_service, role_repository, role_entity
    ):
        """
        Tests retrieving paginated roles.
        """
        print("🧪 Testing retrieving paginated roles...")

        roles = [role_entity, Role(id=2, name="User", created_at=datetime.now())]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=roles, meta=pagination)

        role_repository.get_pageable = AsyncMock(return_value=page_result)

        result = await role_service.get_paginated_roles(page=1, size=10)

        assert isinstance(result, RolePage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        role_repository.get_pageable.assert_called_once_with(page=1, size=10)
        print(
            f"✅ Retrieved paginated roles successfully: {len(result.data)} roles in page {result.meta.current_page}"
        )

    @pytest.mark.asyncio
    async def test_get_paginated_roles_invalid_params(
        self, role_service, role_repository
    ):
        """
        Tests retrieving paginated roles with invalid parameters.
        """
        print("🧪 Testing paginated roles with invalid parameters...")

        # Test invalid page
        with pytest.raises(BadRequestException) as exc_info:
            await role_service.get_paginated_roles(page=0, size=10)
        assert "Page number must be greater than 0" in str(exc_info.value)
        print(
            f"✅ BadRequestException correctly raised for invalid page: {exc_info.value}"
        )

        # Test invalid size
        with pytest.raises(BadRequestException) as exc_info:
            await role_service.get_paginated_roles(page=1, size=0)
        assert "Size number must be greater than 0" in str(exc_info.value)
        print(
            f"✅ BadRequestException correctly raised for invalid size: {exc_info.value}"
        )

    @pytest.mark.asyncio
    async def test_find_success(self, role_service, role_repository, role_entity):
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
            previous_page=None,
        )
        page_result = Page(data=roles, meta=pagination)

        role_repository.find = AsyncMock(return_value=page_result)

        result = await role_service.find(page=1, size=10, search_term="Admin")

        assert isinstance(result, RolePage)
        assert len(result.data) == 1
        assert result.data[0].name == "Administrator"
        assert result.meta.total == 1
        role_repository.find.assert_called_once_with(1, 10, {"name": "Admin"})
        print(f"✅ Search found {len(result.data)} roles for term 'Admin'")
