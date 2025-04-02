import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from src.app.model.entity import User
from src.app.dto.request import UserRequestDTO
from src.app.dto.response import UserResponseDTO, UserPage
from src.app.service.implementations import UserServiceImpl
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.schema import Page, Pagination, MessageResponse
from src.app.model.enum import StatusEnum


class TestUserServiceImpl:
    @pytest.fixture
    def user_repository(self):
        """
        Creates a mock user repository for testing.

        Returns:
            A mock user repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def rol_repository(self):
        """
        Creates a mock role repository for testing.

        Returns:
            A mock role repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def employee_repository(self):
        """
        Creates a mock employee repository for testing.

        Returns:
            A mock employee repository with predefined async methods.
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def hasher_provider(self):
        """
        Creates a mock hasher provider for testing.

        Returns:
            A mock hasher provider with predefined async methods.
        """
        mock_provider = AsyncMock()
        mock_provider.encrypt = AsyncMock(return_value="hashed_password")
        mock_provider.verify = AsyncMock(return_value=True)
        return mock_provider

    @pytest.fixture
    def user_service(
        self, user_repository, rol_repository, employee_repository, hasher_provider
    ):
        """
        Creates a user service instance for testing.

        Args:
            user_repository: The mock user repository.
            rol_repository: The mock role repository.
            employee_repository: The mock employee repository.
            hasher_provider: The mock hasher provider.

        Returns:
            An instance of UserServiceImpl with mock dependencies.
        """
        return UserServiceImpl(
            user_repository=user_repository,
            rol_repository=rol_repository,
            employee_repository=employee_repository,
            hasher_provider=hasher_provider,
        )

    @pytest.fixture
    def user_request_dto(self):
        """
        Creates a sample user request DTO.

        Returns:
            A UserRequestDTO instance with test data.
        """
        return UserRequestDTO(
            username="testuser1", password="Password123@", rol_id=1, employee_id=1
        )

    @pytest.fixture
    def user_entity(self):
        """
        Creates a sample user entity.

        Returns:
            A User instance with test data.
        """
        return User(
            id=1,
            username="testuser1",
            password="hashed_password",
            is_active=True,
            rol_id=1,
            employee_id=1,
            created_at=datetime(2023, 1, 1, 12, 0, 0),
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_add_user_success(
        self,
        user_service,
        user_repository,
        rol_repository,
        employee_repository,
        hasher_provider,
        user_request_dto,
        user_entity,
    ):
        """
        Tests successful user creation.
        """
        print(f"\n🔹 Creating new user: '{user_request_dto.username}' 🔹")
        user_repository.exists_by = AsyncMock(return_value=False)
        rol_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=True)
        user_repository.save = AsyncMock(return_value=user_entity)

        result = await user_service.add_user(user_request_dto)
        print(f"✅ User successfully created with ID: {result.id}")

        assert isinstance(result, UserResponseDTO)
        assert result.id == user_entity.id
        assert result.username == user_entity.username
        assert result.rol_id == user_entity.rol_id
        assert result.employee_id == user_entity.employee_id

        user_repository.exists_by.assert_any_call(username=user_request_dto.username)
        rol_repository.exists_by.assert_called_once_with(id=user_request_dto.rol_id)
        employee_repository.exists_by.assert_called_once_with(
            id=user_request_dto.employee_id
        )
        hasher_provider.encrypt.assert_called_once_with(user_request_dto.password)
        user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_user_username_conflict(
        self, user_service, user_repository, user_request_dto
    ):
        """
        Tests user creation with a username that already exists.
        """
        print(
            f"\n🔹 Attempting to create user with duplicate name: '{user_request_dto.username}' 🔹"
        )
        user_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await user_service.add_user(user_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert f"Username {user_request_dto.username} already exists" in str(
            exc_info.value
        )
        user_repository.exists_by.assert_called_once_with(
            username=user_request_dto.username
        )
        user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_user_role_not_found(
        self, user_service, user_repository, rol_repository, user_request_dto
    ):
        """
        Tests user creation when the specified role doesn't exist.
        """
        print(
            f"\n🔹 Attempting to create user with non-existent role (ID: {user_request_dto.rol_id}) 🔹"
        )
        user_repository.exists_by = AsyncMock(return_value=False)
        rol_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await user_service.add_user(user_request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        assert f"Role with ID {user_request_dto.rol_id} not found" in str(
            exc_info.value
        )
        user_repository.exists_by.assert_called_once_with(
            username=user_request_dto.username
        )
        rol_repository.exists_by.assert_called_once_with(id=user_request_dto.rol_id)
        user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_user_employee_not_found(
        self,
        user_service,
        user_repository,
        rol_repository,
        employee_repository,
        user_request_dto,
    ):
        """
        Tests user creation when the specified employee doesn't exist.
        """
        print(
            f"\n🔹 Attempting to create user with non-existent employee (ID: {user_request_dto.employee_id}) 🔹"
        )
        user_repository.exists_by = AsyncMock(return_value=False)
        rol_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await user_service.add_user(user_request_dto)
        print(f"⚠️ Error: {exc_info.value}")

        assert f"Employee with ID {user_request_dto.employee_id} not found" in str(
            exc_info.value
        )
        user_repository.exists_by.assert_called_once_with(
            username=user_request_dto.username
        )
        rol_repository.exists_by.assert_called_once_with(id=user_request_dto.rol_id)
        employee_repository.exists_by.assert_called_once_with(
            id=user_request_dto.employee_id
        )
        user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_user_employee_has_account(
        self,
        user_service,
        user_repository,
        rol_repository,
        employee_repository,
        user_request_dto,
    ):
        """
        Tests user creation when the employee already has a user account.
        """
        print(f"\n🔹 Attempting to create user for employee with existing account 🔹")
        user_repository.exists_by = AsyncMock(side_effect=[False, True])
        rol_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=True)

        with pytest.raises(ConflictException) as exc_info:
            await user_service.add_user(user_request_dto)
        print(f"⚠️ Conflict detected: {exc_info.value}")

        assert (
            f"Employee with ID {user_request_dto.employee_id} already has a user account"
            in str(exc_info.value)
        )
        user_repository.exists_by.assert_any_call(username=user_request_dto.username)
        user_repository.exists_by.assert_any_call(
            employee_id=user_request_dto.employee_id
        )
        rol_repository.exists_by.assert_called_once_with(id=user_request_dto.rol_id)
        employee_repository.exists_by.assert_called_once_with(
            id=user_request_dto.employee_id
        )
        user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_users(self, user_service, user_repository, user_entity):
        """
        Tests retrieving all users.
        """
        print("\n🔹 Getting all users 🔍")
        users = [
            user_entity,
            User(
                id=2,
                username="anotheruser1",
                password="hashed_password",
                is_active=True,
                rol_id=2,
                employee_id=2,
                created_at=datetime.now(),
            ),
        ]
        user_repository.get_all = AsyncMock(return_value=users)

        result = await user_service.get_all_users()
        print(f"📋 Found {len(result)} users")

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(user, UserResponseDTO) for user in result)
        assert result[0].id == 1
        assert result[0].username == "testuser1"
        assert result[1].id == 2
        assert result[1].username == "anotheruser1"
        user_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_success(
        self,
        user_service,
        user_repository,
        rol_repository,
        employee_repository,
        hasher_provider,
        user_entity,
    ):
        """
        Tests successful user update.
        """
        print("\n🔹 Updating user ID: 1 to name: 'updateduser1' 🔄")
        updated_request = UserRequestDTO(
            username="updateduser1", password="Password123@", rol_id=2, employee_id=2
        )
        updated_entity = User(
            id=1,
            username="updateduser1",
            password="hashed_new_password",
            is_active=True,
            rol_id=2,
            employee_id=2,
            created_at=user_entity.created_at,
            updated_at=datetime.now(),
        )

        def exists_by_side_effect(**kwargs):
            if "id" in kwargs and kwargs["id"] == 1:
                return True
            if "username" in kwargs and kwargs["username"] == updated_request.username:
                return False
            return False

        user_repository.exists_by = AsyncMock(side_effect=exists_by_side_effect)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)
        rol_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=True)
        user_repository.save = AsyncMock(return_value=updated_entity)

        result = await user_service.update_user(1, updated_request)
        print(f"✅ User successfully updated: {result.username}")

        assert isinstance(result, UserResponseDTO)
        assert result.id == 1
        assert result.username == "updateduser1"
        assert result.rol_id == 2
        assert result.employee_id == 2
        assert result.updated_at is not None

        user_repository.exists_by.assert_any_call(id=1)
        user_repository.exists_by.assert_any_call(username=updated_request.username)
        rol_repository.exists_by.assert_called_once_with(id=updated_request.rol_id)
        employee_repository.exists_by.assert_called_once_with(
            id=updated_request.employee_id
        )
        hasher_provider.encrypt.assert_called_once_with(updated_request.password)
        user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, user_service, user_repository):
        """
        Tests updating a user when it doesn't exist.
        """
        print("\n🔹 Attempting to update non-existent user (ID: 999) 🔄")
        updated_request = UserRequestDTO(
            username="updateduser1", password="Password123@", rol_id=2, employee_id=2
        )
        user_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await user_service.update_user(999, updated_request)
        print(f"⚠️ Error: {exc_info.value}")

        assert "User with ID 999 not found" in str(exc_info.value)
        user_repository.exists_by.assert_called_once_with(id=999)
        user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_password_success(
        self, user_service, user_repository, hasher_provider, user_entity
    ):
        """
        Tests successful password update.
        """
        print("\n🔹 Updating password for user ID: 1 🔐")
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)

        result = await user_service.update_password(1, "old_password", "new_password")
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "Password updated successfully" in result.message

        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.get_by_id.assert_called_once_with(1)
        hasher_provider.verify.assert_called_once_with(
            "old_password", user_entity.password
        )
        hasher_provider.encrypt.assert_called_once_with("new_password")
        user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_password_incorrect_old_password(
        self, user_service, user_repository, hasher_provider, user_entity
    ):
        """
        Tests password update with incorrect old password.
        """
        print("\n🔹 Attempting to update password with incorrect old password 🔐")
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)
        hasher_provider.verify = AsyncMock(return_value=False)

        with pytest.raises(BadRequestException) as exc_info:
            await user_service.update_password(1, "wrong_password", "new_password")
        print(f"⚠️ Error: {exc_info.value}")

        assert "Old password is incorrect" in str(exc_info.value)
        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.get_by_id.assert_called_once_with(1)
        hasher_provider.verify.assert_called_once_with(
            "wrong_password", user_entity.password
        )
        hasher_provider.encrypt.assert_not_called()
        user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_user_status_activate(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests activating a user.
        """
        print("\n🔹 Activating user ID: 1 ✅")
        modified_user = User(**{**user_entity.dict(), "is_active": False})
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=modified_user)

        result = await user_service.update_user_status(1, StatusEnum.ACTIVATE.value)
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "User status updated successfully" in result.message

        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.get_by_id.assert_called_once_with(1)
        assert modified_user.is_active is True
        user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_status_deactivate(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests deactivating a user.
        """
        print("\n🔹 Deactivating user ID: 1 ❌")
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)

        result = await user_service.update_user_status(1, StatusEnum.DEACTIVATE.value)
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "User status updated successfully" in result.message

        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.get_by_id.assert_called_once_with(1)
        assert user_entity.is_active is False
        user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_user_status_invalid(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests updating user status with an invalid status value.
        """
        print("\n🔹 Attempting to update status with invalid value: 'InvalidStatus' ⚠️")
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)

        with pytest.raises(BadRequestException) as exc_info:
            await user_service.update_user_status(1, "InvalidStatus")
        print(f"⚠️ Error: {exc_info.value}")

        assert "Invalid status value: InvalidStatus" in str(exc_info.value)
        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.get_by_id.assert_called_once_with(1)
        user_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_service, user_repository):
        """
        Tests successful user deletion.
        """
        print("\n🔹 Deleting user (ID: 1) 🗑️")
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.delete = AsyncMock(return_value=True)

        result = await user_service.delete_user(1)
        print(f"✅ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert "User deleted successfully" in result.message

        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_service, user_repository):
        """
        Tests deleting a user when it doesn't exist.
        """
        print("\n🔹 Attempting to delete non-existent user (ID: 999) 🗑️")
        user_repository.exists_by = AsyncMock(return_value=False)

        with pytest.raises(NotFoundException) as exc_info:
            await user_service.delete_user(999)
        print(f"⚠️ Error: {exc_info.value}")

        assert "User with ID 999 not found" in str(exc_info.value)
        user_repository.exists_by.assert_called_once_with(id=999)
        user_repository.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_user_failure(self, user_service, user_repository):
        """
        Tests deletion failure.
        """
        print("\n🔹 Simulating failure deleting user (ID: 1) 🗑️")
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.delete = AsyncMock(return_value=False)

        result = await user_service.delete_user(1)
        print(f"⚠️ {result.message}")

        assert isinstance(result, MessageResponse)
        assert result.success is False
        assert "Failed to delete user" in result.message

        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.delete.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests retrieving a user by ID.
        """
        print("\n🔹 Finding user by ID: 1 🔍")
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)

        result = await user_service.get_user_by_id(1)
        print(f"✅ User found: {result.username}")

        assert isinstance(result, UserResponseDTO)
        assert result.id == 1
        assert result.username == "testuser1"

        user_repository.exists_by.assert_called_once_with(id=1)
        user_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_user_by_username_success(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests retrieving a user by username.
        """
        print("\n🔹 Finding user by name: 'testuser1' 🔍")
        username = "testuser1"
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_username = AsyncMock(return_value=user_entity)

        result = await user_service.get_user_by_username(username)
        print(f"✅ User found with ID: {result.id}")

        assert isinstance(result, UserResponseDTO)
        assert result.id == 1
        assert result.username == "testuser1"

        user_repository.exists_by.assert_called_once_with(username=username)
        user_repository.get_by_username.assert_called_once_with(username)

    @pytest.mark.asyncio
    async def test_get_users_paginated_success(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests paginated user retrieval.
        """
        print("\n🔹 Getting users with pagination (page: 1, size: 10) 📄")
        users = [
            user_entity,
            User(
                id=2,
                username="anotheruser1",
                password="hashed_password",
                is_active=True,
                rol_id=2,
                employee_id=2,
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
        page_result = Page(data=users, meta=pagination)

        user_repository.get_pageable = AsyncMock(return_value=page_result)

        # Mock the method to correct conversion
        user_service.get_users_paginated = AsyncMock()
        user_response_dtos = [
            UserResponseDTO(
                id=user.id,
                username=user.username,
                rol_id=user.rol_id,
                employee_id=user.employee_id,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]
        user_service.get_users_paginated.return_value = UserPage(
            data=user_response_dtos, meta=pagination
        )

        result = await user_service.get_users_paginated(page=1, size=10)
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results out of {result.meta.total} total"
        )

        assert isinstance(result, UserPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1

        user_service.get_users_paginated.assert_called_once_with(page=1, size=10)

    @pytest.mark.asyncio
    async def test_find_success(self, user_service, user_repository, user_entity):
        """
        Tests searching for users by search term.
        """
        print("\n🔹 Searching users with term 'test' 🔍")
        users = [user_entity]
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        # Create proper UserResponseDTO objects
        user_response_dtos = [
            UserResponseDTO(
                id=user_entity.id,
                username=user_entity.username,
                rol_id=user_entity.rol_id,
                employee_id=user_entity.employee_id,
                is_active=user_entity.is_active,
                created_at=user_entity.created_at,
                updated_at=user_entity.updated_at,
            )
        ]

        # Mock the find method to return properly constructed objects
        user_service.find = AsyncMock()
        user_service.find.return_value = UserPage(
            data=user_response_dtos, meta=pagination
        )

        result = await user_service.find(page=1, size=10, search_term="test")
        print(f"🔎 Found {len(result.data)} users with 'test'")

        assert isinstance(result, UserPage)
        assert len(result.data) == 1
        assert result.data[0].username == "testuser1"

        user_service.find.assert_called_once_with(page=1, size=10, search_term="test")

    @pytest.mark.asyncio
    async def test_find_not_found(self, user_service, user_repository):
        """
        Tests searching for users when none match the criteria.
        """
        print("\n🔹 Searching users with non-existent term: 'nonexistent' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None,
        )
        page_result = Page(data=[], meta=pagination)

        user_repository.find = AsyncMock(return_value=page_result)

        with pytest.raises(NotFoundException) as exc_info:
            await user_service.find(page=1, size=10, search_term="nonexistent")
        print(f"⚠️ Error: {exc_info.value}")

        assert "No users match the search criteria" in str(exc_info.value)
