import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from src.repository.implementations import RolRepositoryImpl
from src.model.entity import Rol
from src.exception import DatabaseException, InvalidFieldException
from src.schema import Page, Pagination


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def rol_repository(mock_session):
    return RolRepositoryImpl(session=mock_session)


@pytest.fixture
def rol_sample():
    return Rol(
        id=1,
        nombre="Administrador",
        created_at=datetime.now(),
        updated_at=None
    )


class TestRolRepositoryImpl:

    @pytest.mark.asyncio
    async def test_save_success(self, rol_repository, mock_session, rol_sample):
        """Test to verify that the save method correctly stores a role."""
        print("🧪 Testing successful role saving...")

        result = await rol_repository.save(rol_sample)

        mock_session.add.assert_called_once_with(rol_sample)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(rol_sample)
        assert result == rol_sample
        print(f"✅ Role saved successfully: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_save_integrity_error(self, rol_repository, mock_session, rol_sample):
        """Test to verify that the save method correctly handles integrity errors."""
        print("🧪 Testing integrity error handling during save...")

        error_original = MagicMock()
        error_original.__str__.return_value = "Duplicate entry"

        mock_session.add = AsyncMock()
        mock_session.commit.side_effect = IntegrityError("Duplicate entry", None, error_original)

        with pytest.raises(DatabaseException) as exc_info:
            await rol_repository.save(rol_sample)

        assert "Error de integridad de datos" in str(exc_info.value)
        mock_session.rollback.assert_called_once()
        print(f"✅ Integrity error correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_get_all_success(self, rol_repository, mock_session):
        """Test to verify that get_all returns all roles."""
        print("🧪 Testing retrieval of all roles...")

        roles = [
            Rol(id=1, nombre="Administrador"),
            Rol(id=2, nombre="Usuario")
        ]

        rol_repository.get_all = AsyncMock(return_value=roles)

        result = await rol_repository.get_all()

        assert len(result) == 2
        assert result[0].nombre == "Administrador"
        assert result[1].nombre == "Usuario"
        print(f"✅ All roles retrieved: {len(result)} roles found")
        for i, rol in enumerate(result):
            print(f"   - Role {i + 1}: ID={rol.id}, Name='{rol.nombre}'")

    @pytest.mark.asyncio
    async def test_delete_success(self, rol_repository, mock_session, rol_sample):
        """Test to verify that delete correctly removes a role."""
        print("🧪 Testing role deletion...")

        rol_repository.get_by_id = AsyncMock(return_value=rol_sample)

        result = await rol_repository.delete(1)

        assert result is True
        mock_session.delete.assert_called_once_with(rol_sample)
        mock_session.commit.assert_called_once()
        print(f"✅ Role deleted successfully: ID=1, Name='{rol_sample.nombre}'")

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, rol_repository, mock_session, rol_sample):
        """Test to verify that get_by_id returns the correct role."""
        print("🧪 Testing role retrieval by ID...")

        rol_repository.get_by_id = AsyncMock(return_value=rol_sample)

        result = await rol_repository.get_by_id(1)

        assert result == rol_sample
        assert result.nombre == "Administrador"
        print(f"✅ Role retrieved by ID: ID={result.id}, Name='{result.nombre}'")

    @pytest.mark.asyncio
    async def test_get_pageable_success(self, rol_repository, mock_session):
        """Test to verify that get_pageable returns a page of results."""
        print("🧪 Testing role pagination...")

        roles = [
            Rol(id=1, nombre="Administrador"),
            Rol(id=2, nombre="Usuario")
        ]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=2,
            total_pages=1,
            next_page=None,
            previous_page=None
        )

        pagina = Page(
            data=roles,
            meta=pagination_info
        )

        rol_repository.get_pageable = AsyncMock(return_value=pagina)

        result = await rol_repository.get_pageable(page=1, size=10)

        assert isinstance(result, Page)
        assert len(result.data) == 2
        assert result.meta.total == 2
        assert result.meta.current_page == 1
        print(f"✅ Roles paginated: Page {result.meta.current_page}/{result.meta.total_pages}, "
              f"showing {len(result.data)} of {result.meta.total} roles")
        for i, rol in enumerate(result.data):
            print(f"   - Role {i + 1}: ID={rol.id}, Name='{rol.nombre}'")

    @pytest.mark.asyncio
    async def test_exists_by_success(self, rol_repository, mock_session):
        """Test to verify that exists_by returns True when the role exists."""
        print("🧪 Testing role existence verification...")

        rol_repository.exists_by = AsyncMock(return_value=True)

        result = await rol_repository.exists_by(nombre="Administrador")

        assert result is True
        print(f"✅ Role existence verified: 'Administrador' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_not_found(self, rol_repository, mock_session):
        """Test to verify that exists_by returns False when the role doesn't exist."""
        print("🧪 Testing non-existent role verification...")

        rol_repository.exists_by = AsyncMock(return_value=False)

        result = await rol_repository.exists_by(nombre="Rol Inexistente")

        assert result is False
        print(f"✅ Role non-existence verified: 'Rol Inexistente' exists = {result}")

    @pytest.mark.asyncio
    async def test_exists_by_invalid_field(self, rol_repository):
        """Test to verify that exists_by throws an exception with invalid field."""
        print("🧪 Testing invalid field handling...")

        rol_repository.exists_by = AsyncMock(side_effect=InvalidFieldException("Invalid field"))

        with pytest.raises(InvalidFieldException) as exc_info:
            await rol_repository.exists_by(campo_inexistente="valor")

        print(f"✅ Invalid field correctly handled: {exc_info.value}")

    @pytest.mark.asyncio
    async def test_find_with_filters(self, rol_repository, mock_session):
        """Test to verify that find correctly filters by search criteria."""
        print("🧪 Testing search with filters...")

        roles = [Rol(id=1, nombre="Administrador")]

        pagination_info = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=None,
            previous_page=None
        )

        pagina = Page(
            data=roles,
            meta=pagination_info
        )

        rol_repository.find = AsyncMock(return_value=pagina)

        search_params = {"nombre": "admin"}
        result = await rol_repository.find(page=1, size=10, search_dict=search_params)

        assert isinstance(result, Page)
        assert len(result.data) == 1
        assert result.data[0].nombre == "Administrador"
        assert result.meta.total == 1
        print(f"✅ Search with filters successful: Found {result.meta.total} results for criteria {search_params}")
        for i, rol in enumerate(result.data):
            print(f"   - Result {i + 1}: ID={rol.id}, Name='{rol.nombre}'")