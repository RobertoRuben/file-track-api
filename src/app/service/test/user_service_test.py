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

        :return: A mock user repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def role_repository(self):
        """
        Creates a mock role repository for testing.

        :return: A mock role repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def employee_repository(self):
        """
        Creates a mock employee repository for testing.

        :return: A mock employee repository with predefined async methods
        """
        mock_repository = AsyncMock()
        return mock_repository

    @pytest.fixture
    def hasher_provider(self):
        """
        Creates a mock password hasher provider for testing.

        :return: A mock hasher provider with predefined async methods
        """
        mock_provider = AsyncMock()
        mock_provider.encrypt = AsyncMock(return_value="hashed_password")
        mock_provider.verify = AsyncMock(return_value=True)
        return mock_provider

    @pytest.fixture
    def user_service(
        self, user_repository, role_repository, employee_repository, hasher_provider
    ):
        """
        Creates a user service instance with mock dependencies for testing.

        :param user_repository: Mock user repository
        :param role_repository: Mock role repository
        :param employee_repository: Mock employee repository
        :param hasher_provider: Mock password hasher provider
        :return: A UserServiceImpl instance for testing
        """
        return UserServiceImpl(
            user_repository=user_repository,
            role_repository=role_repository,
            employee_repository=employee_repository,
            hasher_provider=hasher_provider,
        )

    @pytest.fixture
    def user_request_dto(self):
        """
        Creates a sample user request DTO for testing.

        :return: A UserRequestDTO with test data
        """
        return UserRequestDTO(
            username="jdoe123",
            password="Secret@123",
            is_active=StatusEnum.ACTIVATE,
            role_id=1,
            employee_id=1,
        )

    @pytest.fixture
    def user_entity(self):
        """
        Creates a sample user entity for testing.

        :return: A User entity with test data
        """
        return User(
            id=1,
            username="jdoe123",
            password="hashed_password",
            is_active=True,
            role_id=1,
            employee_id=1,
            created_at=datetime.now(),
            updated_at=None,
        )

    @pytest.mark.asyncio
    async def test_add_user_success(
        self,
        user_service,
        user_repository,
        role_repository,
        employee_repository,
        user_request_dto,
        user_entity,
    ):
        """
        Tests the successful addition of a new user.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param role_repository: Mock role repository
        :param employee_repository: Mock employee repository
        :param user_request_dto: Sample user request DTO
        :param user_entity: Sample user entity
        """
        print("\n🔹 Adding new user: jdoe123 ➕")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(side_effect=[False, False])
        role_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=True)
        user_repository.save = AsyncMock(return_value=user_entity)

        # Execute the test
        result = await user_service.add_user(user_request_dto)

        # Verify the result
        assert isinstance(result, UserResponseDTO)
        assert result.id == 1
        assert result.username == "jdoe123"
        print(
            f"✅ User added successfully: ID={result.id}, Username='{result.username}'"
        )

    @pytest.mark.asyncio
    async def test_add_user_username_conflict(
        self, user_service, user_repository, user_request_dto
    ):
        """
        Tests adding a user with an existing username.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_request_dto: Sample user request DTO
        """
        print("\n🔹 Adding user with existing username: jdoe123 ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)

        # Execute the test and verify the exception
        with pytest.raises(ConflictException) as exc_info:
            await user_service.add_user(user_request_dto)

        print(f"⚠️ Error: {exc_info.value}")
        assert "already exists" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_add_user_role_not_found(
        self, user_service, user_repository, role_repository, user_request_dto
    ):
        """
        Tests adding a user with a non-existent role.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param role_repository: Mock role repository
        :param user_request_dto: Sample user request DTO
        """
        print("\n🔹 Adding user with non-existent role: 999 ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=False)
        role_repository.exists_by = AsyncMock(return_value=False)

        # Execute the test and verify the exception
        with pytest.raises(NotFoundException) as exc_info:
            await user_service.add_user(user_request_dto)

        print(f"⚠️ Error: {exc_info.value}")
        assert "Role with ID" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_add_user_employee_not_found(
        self,
        user_service,
        user_repository,
        role_repository,
        employee_repository,
        user_request_dto,
    ):
        """
        Tests adding a user with a non-existent employee.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param role_repository: Mock role repository
        :param employee_repository: Mock employee repository
        :param user_request_dto: Sample user request DTO
        """
        print("\n🔹 Adding user with non-existent employee: 999 ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=False)
        role_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=False)

        # Execute the test and verify the exception
        with pytest.raises(NotFoundException) as exc_info:
            await user_service.add_user(user_request_dto)

        print(f"⚠️ Error: {exc_info.value}")
        assert "Employee with ID" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_add_user_employee_has_account(
        self,
        user_service,
        user_repository,
        role_repository,
        employee_repository,
        user_request_dto,
    ):
        """
        Tests adding a user for an employee who already has a user account.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param role_repository: Mock role repository
        :param employee_repository: Mock employee repository
        :param user_request_dto: Sample user request DTO
        """
        print("\n🔹 Adding user for employee who already has an account ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(side_effect=[False, True])
        role_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=True)

        # Execute the test and verify the exception
        with pytest.raises(ConflictException) as exc_info:
            await user_service.add_user(user_request_dto)

        print(f"⚠️ Error: {exc_info.value}")
        assert "already has a user account" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_all_users(self, user_service, user_repository, user_entity):
        """
        Tests retrieving all users.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_entity: Sample user entity
        """
        print("\n🔹 Getting all users 📋")

        # Set up mock behavior
        users = [
            user_entity,
            User(
                id=2,
                username="asmith456",
                password="hashed_password",
                is_active=True,
                role_id=2,
                employee_id=2,
                created_at=datetime.now(),
                updated_at=None,
            ),
        ]
        user_repository.get_all = AsyncMock(return_value=users)

        # Execute the test
        result = await user_service.get_all_users()

        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(user, UserResponseDTO) for user in result)
        print(f"✅ Retrieved {len(result)} users")
        for i, user in enumerate(result):
            print(f"   - User {i+1}: ID={user.id}, Username='{user.username}'")

    @pytest.mark.asyncio
    async def test_update_user_success(
        self,
        user_service,
        user_repository,
        role_repository,
        employee_repository,
        user_request_dto,
        user_entity,
    ):
        """
        Tests the successful update of a user.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param role_repository: Mock role repository
        :param employee_repository: Mock employee repository
        :param user_request_dto: Sample user request DTO
        :param user_entity: Sample user entity
        """
        print("\n🔹 Updating user: ID=1 ✏️")

        # Configurar el comportamiento del mock para que devuelva diferentes valores
        # dependiendo de los parámetros recibidos
        async def exists_by_side_effect(**kwargs):
            if 'id' in kwargs and kwargs['id'] == 1:
                return True  # El usuario con ID=1 existe
            if 'username' in kwargs and kwargs['username'] == "jdoe_updated45":
                return False  # No existe usuario con el nuevo username
            return False

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(side_effect=exists_by_side_effect)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)
        role_repository.exists_by = AsyncMock(return_value=True)
        employee_repository.exists_by = AsyncMock(return_value=True)

        # Configurar el mock de save para devolver un usuario actualizado
        updated_entity = User(
            id=1,
            username="jdoe_updated45",  # Nombre actualizado
            password="hashed_password",  # La contraseña se encriptará
            is_active=True,
            role_id=2,  # Rol actualizado
            employee_id=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),  # Ahora tiene fecha de actualización
        )
        user_repository.save = AsyncMock(return_value=updated_entity)

        # Update user data
        updated_request = UserRequestDTO(
            username="jdoe_updated45",
            password="NewSecret@123",
            is_active=StatusEnum.ACTIVATE,
            role_id=2,
            employee_id=1,
        )

        # Execute the test
        result = await user_service.update_user(1, updated_request)

        # Verify the result
        assert isinstance(result, UserResponseDTO)
        assert result.id == 1
        assert (
            result.username == "jdoe_updated45"
        )  # Verificar que el nombre se actualizó
        assert result.role_id == 2  # Verificar que el rol se actualizó
        print(
            f"✅ User updated successfully: ID={result.id}, Username='{result.username}'"
        )

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, user_service, user_repository):
        """
        Tests updating a non-existent user.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        """
        print("\n🔹 Updating non-existent user: ID=999 ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=False)

        # Create a sample update request
        update_request = UserRequestDTO(
            username="test_user",
            password="Secret@123",
            is_active=StatusEnum.ACTIVATE,
            role_id=1,
            employee_id=1,
        )

        # Execute the test and verify the exception
        with pytest.raises(NotFoundException) as exc_info:
            await user_service.update_user(999, update_request)

        print(f"⚠️ Error: {exc_info.value}")
        assert "User with ID 999 not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_password_success(
        self, user_service, user_repository, hasher_provider, user_entity
    ):
        """
        Tests the successful update of a user's password.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param hasher_provider: Mock password hasher provider
        :param user_entity: Sample user entity
        """
        print("\n🔹 Updating user password: ID=1 🔑")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)
        hasher_provider.verify = AsyncMock(return_value=True)
        hasher_provider.encrypt = AsyncMock(return_value="new_hashed_password")
        user_repository.save = AsyncMock(return_value=user_entity)

        # Execute the test
        result = await user_service.update_password(1, "OldSecret@123", "NewSecret@123")

        # Verify the result
        assert isinstance(result, MessageResponse)
        assert result.success is True
        print(f"✅ Password updated: {result.message}")

    @pytest.mark.asyncio
    async def test_update_password_incorrect_old_password(
        self, user_service, user_repository, hasher_provider, user_entity
    ):
        """
        Tests updating a password with an incorrect old password.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param hasher_provider: Mock password hasher provider
        :param user_entity: Sample user entity
        """
        print("\n🔹 Updating password with incorrect old password ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)
        hasher_provider.verify = AsyncMock(return_value=False)

        # Execute the test and verify the exception
        with pytest.raises(BadRequestException) as exc_info:
            await user_service.update_password(1, "WrongPassword", "NewSecret@123")

        print(f"⚠️ Error: {exc_info.value}")
        assert "Old password is incorrect" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_update_user_status_activate(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests activating a user account.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_entity: Sample user entity
        """
        print("\n🔹 Activating user: ID=1 ✅")

        # Modify the entity for this test
        user_entity.is_active = False

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)
        user_repository.save = AsyncMock(return_value=user_entity)

        # Execute the test
        result = await user_service.update_user_status(1, StatusEnum.ACTIVATE.value)

        # Verify the result
        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert user_entity.is_active is True
        print(f"✅ User activated: {result.message}")

    @pytest.mark.asyncio
    async def test_update_user_status_deactivate(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests deactivating a user account.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_entity: Sample user entity
        """
        print("\n🔹 Deactivating user: ID=1 ❌")

        # Ensure the entity is active for this test
        user_entity.is_active = True

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)
        user_repository.save = AsyncMock(return_value=user_entity)

        # Execute the test
        result = await user_service.update_user_status(1, StatusEnum.DEACTIVATE.value)

        # Verify the result
        assert isinstance(result, MessageResponse)
        assert result.success is True
        assert user_entity.is_active is False
        print(f"✅ User deactivated: {result.message}")

    @pytest.mark.asyncio
    async def test_update_user_status_invalid(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests updating a user's status with an invalid status value.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_entity: Sample user entity
        """
        print("\n🔹 Updating user status with invalid value ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)

        # Execute the test and verify the exception
        with pytest.raises(BadRequestException) as exc_info:
            await user_service.update_user_status(1, "InvalidStatus")

        print(f"⚠️ Error: {exc_info.value}")
        assert "Invalid status value" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_service, user_repository):
        """
        Tests the successful deletion of a user.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        """
        print("\n🔹 Deleting user: ID=1 🗑️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.delete = AsyncMock(return_value=True)

        # Execute the test
        result = await user_service.delete_user(1)

        # Verify the result
        assert isinstance(result, MessageResponse)
        assert result.success is True
        print(f"✅ User deleted: {result.message}")

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, user_service, user_repository):
        """
        Tests deleting a non-existent user.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        """
        print("\n🔹 Deleting non-existent user: ID=999 ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=False)

        # Execute the test and verify the exception
        with pytest.raises(NotFoundException) as exc_info:
            await user_service.delete_user(999)

        print(f"⚠️ Error: {exc_info.value}")
        assert "User with ID 999 not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_delete_user_failure(self, user_service, user_repository):
        """
        Tests a failed user deletion.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        """
        print("\n🔹 Testing deletion failure scenario ⚠️")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.delete = AsyncMock(return_value=False)

        # Execute the test
        result = await user_service.delete_user(1)

        # Verify the result
        assert isinstance(result, MessageResponse)
        assert result.success is False
        print(f"✅ Deletion failure correctly handled: {result.message}")

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests retrieving a user by ID.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_entity: Sample user entity
        """
        print("\n🔹 Getting user by ID: 1 🔍")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_id = AsyncMock(return_value=user_entity)

        # Execute the test
        result = await user_service.get_user_by_id(1)

        # Verify the result
        assert isinstance(result, UserResponseDTO)
        assert result.id == 1
        assert result.username == "jdoe123"
        print(f"✅ User retrieved: ID={result.id}, Username='{result.username}'")

    @pytest.mark.asyncio
    async def test_get_user_by_username_success(
        self, user_service, user_repository, user_entity
    ):
        """
        Tests retrieving a user by username.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_entity: Sample user entity
        """
        print("\n🔹 Getting user by username: 'jdoe123' 🔍")

        # Set up mock behavior
        user_repository.exists_by = AsyncMock(return_value=True)
        user_repository.get_by_username = AsyncMock(return_value=user_entity)

        # Execute the test
        result = await user_service.get_user_by_username("jdoe123")

        # Verify the result
        assert isinstance(result, UserResponseDTO)
        assert result.id == 1
        assert result.username == "jdoe123"
        print(f"✅ User retrieved: ID={result.id}, Username='{result.username}'")

    @pytest.mark.asyncio
    async def test_get_users_paginated_success(self, user_service, user_repository):
        """
        Tests retrieving users with pagination.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        """
        print("\n🔹 Getting paginated users: page=1, size=10 📄")

        # Set up mock data
        users_data = [
            {
                "id": 1,
                "username": "jdoe123",
                "employee_id": 1,
                "employee_name": "John Doe",
                "is_active": True,
                "role_id": 1,
                "role_name": "Administrator",
                "created_at": datetime.now(),
                "updated_at": None,
            },
            {
                "id": 2,
                "username": "asmith456",
                "employee_id": 2,
                "employee_name": "Alice Smith",
                "is_active": True,
                "role_id": 2,
                "role_name": "User",
                "created_at": datetime.now(),
                "updated_at": None,
            },
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=users_data, meta=pagination_info)

        # Set up mock behavior
        user_repository.get_pageable = AsyncMock(return_value=page)

        # Execute the test
        result = await user_service.get_users_paginated(1, 10)

        # Verify the result
        assert isinstance(result, UserPage)
        assert len(result.data) == 2
        assert result.meta.total == 2
        print(
            f"✅ Users paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
            f"showing {len(result.data)} of {result.meta.total} users"
        )
        for i, user in enumerate(result.data):
            print(f"   - User {i+1}: ID={user.id}, Username='{user.username}'")

    @pytest.mark.asyncio
    async def test_find_success(self, user_service, user_repository, user_entity):
        """
        Tests searching for users with a search term.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        :param user_entity: Sample user entity
        """
        print("\n🔹 Searching users with term: 'admin' 🔍")

        # Set up mock data
        users_data = [
            {
                "id": 1,
                "username": "admin123",
                "employee_id": 1,
                "employee_name": "System Administrator",
                "is_active": True,
                "role_id": 1,
                "role_name": "Administrator",
                "created_at": datetime.now(),
                "updated_at": None,
            }
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None,
        )

        page = Page(data=users_data, meta=pagination_info)

        # Set up mock behavior
        user_repository.find = AsyncMock(return_value=page)

        # Execute the test
        result = await user_service.find(1, 10, "admin")

        # Verify the result
        assert isinstance(result, UserPage)
        assert len(result.data) == 1
        assert result.data[0].username == "admin123"
        assert result.meta.total == 1
        print(
            f"✅ Search successful: Found {result.meta.total} results for term 'admin'"
        )
        for i, user in enumerate(result.data):
            print(f"   - Result {i + 1}: ID={user.id}, Username='{user.username}'")

    @pytest.mark.asyncio
    async def test_find_not_found(self, user_service, user_repository):
        """
        Tests searching for users when none match the criteria.

        :param user_service: The service under test
        :param user_repository: Mock user repository
        """
        print("\n🔹 Searching users with non-existent term: 'nonexistent' 🔍")

        # Set up mock data
        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=0,
            total_pages=0,
            next_page=None,
            previous_page=None,
        )

        page_result = Page(data=[], meta=pagination_info)

        # Set up mock behavior
        user_repository.find = AsyncMock(return_value=page_result)

        # Execute the test and verify the exception
        with pytest.raises(NotFoundException) as exc_info:
            await user_service.find(1, 10, "nonexistent")

        print(f"⚠️ Error: {exc_info.value}")
        assert "No users match the search criteria" in str(exc_info.value)
