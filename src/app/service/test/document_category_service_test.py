import pytest
from unittest.mock import AsyncMock
from datetime import datetime
import pytest_asyncio

from src.app.model.entity import DocumentCategory
from src.app.dto.request import DocumentCategoryRequestDTO
from src.app.dto.response import DocumentCategoryResponseDTO, DocumentCategoryPage
from src.app.schema import MessageResponse, Pagination, Page
from src.app.exception import ConflictException, NotFoundException, BadRequestException
from src.app.service.implementations import DocumentCategoryServiceImpl


@pytest.fixture
def mock_repository():
    repository = AsyncMock()
    return repository


@pytest_asyncio.fixture
async def document_category_service(mock_repository):
    return DocumentCategoryServiceImpl(document_category_repository=mock_repository)


@pytest.fixture
def sample_document_category():
    return DocumentCategory(
        id=1,
        name="Legal Documents",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def sample_request_dto():
    return DocumentCategoryRequestDTO(name="Legal Documents")


class TestDocumentCategoryServiceImpl:

    @pytest.mark.asyncio
    async def test_add_document_category_success(
        self,
        document_category_service,
        mock_repository,
        sample_document_category,
        sample_request_dto,
    ):
        print(f"\n🔹 Creating new document category: '{sample_request_dto.name}' 🔹")
        mock_repository.exists_by.return_value = False
        mock_repository.save.return_value = sample_document_category

        result = await document_category_service.add_document_category(
            sample_request_dto
        )
        print(f"✅ Category created successfully with ID: {result.id}")

        mock_repository.exists_by.assert_called_once_with(name=sample_request_dto.name)
        mock_repository.save.assert_called_once()
        assert isinstance(result, DocumentCategoryResponseDTO)
        assert result.id == sample_document_category.id
        assert result.name == sample_document_category.name

    @pytest.mark.asyncio
    async def test_add_document_category_conflict(
        self, document_category_service, mock_repository, sample_request_dto
    ):
        print(
            f"\n🔹 Attempting to create duplicate category: '{sample_request_dto.name}' 🔹"
        )
        mock_repository.exists_by.return_value = True

        with pytest.raises(ConflictException) as exc:
            await document_category_service.add_document_category(sample_request_dto)
        print(f"⚠️ Conflict detected: {exc.value.detail}")

        mock_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_document_categories(
        self, document_category_service, mock_repository, sample_document_category
    ):
        print("\n🔹 Getting all document categories 🔍")
        mock_repository.get_all.return_value = [sample_document_category]

        result = await document_category_service.get_all_document_categories()
        print(f"📋 Found {len(result)} categories")

        mock_repository.get_all.assert_called_once()
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], DocumentCategoryResponseDTO)
        assert result[0].id == sample_document_category.id

    @pytest.mark.asyncio
    async def test_update_document_category_same_name(
        self,
        document_category_service,
        mock_repository,
        sample_document_category,
        sample_request_dto,
    ):
        print(
            f"\n🔹 Updating category ID: 1 keeping name: '{sample_request_dto.name}' 🔄"
        )
        mock_repository.exists_by.return_value = True  # Only verifies ID
        mock_repository.get_by_id.return_value = sample_document_category
        mock_repository.save.return_value = sample_document_category

        result = await document_category_service.update_document_category(
            1, sample_request_dto
        )
        print(f"✅ Category updated successfully: {result.name}")

        assert mock_repository.exists_by.call_count == 1  # Only one call to verify ID
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.save.assert_called_once()
        assert isinstance(result, DocumentCategoryResponseDTO)

    @pytest.mark.asyncio
    async def test_update_document_category_different_name(
        self, document_category_service, mock_repository, sample_document_category
    ):
        different_name_dto = DocumentCategoryRequestDTO(name="Financial Documents")

        print(
            f"\n🔹 Changing category ID: 1 name from '{sample_document_category.name}' to '{different_name_dto.name}' 🔄"
        )

        mock_repository.exists_by.side_effect = [
            True,
            False,
        ]  # First verifies ID, then name
        mock_repository.get_by_id.return_value = sample_document_category

        updated_document = DocumentCategory(
            id=1,
            name="Financial Documents",
            created_at=sample_document_category.created_at,
            updated_at=datetime.now(),
        )
        mock_repository.save.return_value = updated_document

        result = await document_category_service.update_document_category(
            1, different_name_dto
        )
        print(f"✅ Name changed successfully to: '{result.name}'")

        assert mock_repository.exists_by.call_count == 2
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.save.assert_called_once()
        assert isinstance(result, DocumentCategoryResponseDTO)
        assert result.name == "Financial Documents"

    @pytest.mark.asyncio
    async def test_update_document_category_not_found(
        self, document_category_service, mock_repository, sample_request_dto
    ):
        print(f"\n🔹 Attempting to update non-existent category (ID: 999) 🔄")
        mock_repository.exists_by.return_value = False

        with pytest.raises(NotFoundException) as exc:
            await document_category_service.update_document_category(
                999, sample_request_dto
            )
        print(f"⚠️ Error: {exc.value.detail}")

    @pytest.mark.asyncio
    async def test_delete_document_category_success(
        self, document_category_service, mock_repository
    ):
        print("\n🔹 Deleting document category (ID: 1) 🗑️")
        mock_repository.exists_by.return_value = True
        mock_repository.delete.return_value = True

        result = await document_category_service.delete_document_category(1)
        print(f"✅ {result.detail} - {result.details}")

        mock_repository.exists_by.assert_called_once_with(id=1)
        mock_repository.delete.assert_called_once_with(1)
        assert isinstance(result, MessageResponse)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_get_document_category_by_id_success(
        self, document_category_service, mock_repository, sample_document_category
    ):
        print("\n🔹 Finding document category by ID: 1 🔍")
        mock_repository.exists_by.return_value = True
        mock_repository.get_by_id.return_value = sample_document_category

        result = await document_category_service.get_document_category_by_id(1)
        print(f"✅ Category found: '{result.name}'")

        mock_repository.exists_by.assert_called_once_with(id=1)
        mock_repository.get_by_id.assert_called_once_with(1)
        assert isinstance(result, DocumentCategoryResponseDTO)
        assert result.id == sample_document_category.id

    @pytest.mark.asyncio
    async def test_get_paginated_document_categories(
        self, document_category_service, mock_repository, sample_document_category
    ):
        print("\n🔹 Getting document categories with pagination (page: 1, size: 10) 📄")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=0,
            previous_page=0,
        )
        page_result = Page(data=[sample_document_category], meta=pagination)

        mock_repository.get_pageable.return_value = page_result

        result = await document_category_service.get_paginated_document_categories(
            1, 10
        )
        print(
            f"📋 Page {result.meta.current_page} of {result.meta.total_pages}, {len(result.data)} results of {result.meta.total} total"
        )

        mock_repository.get_pageable.assert_called_once_with(1, 10)
        assert isinstance(result, DocumentCategoryPage)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_find_success(
        self, document_category_service, mock_repository, sample_document_category
    ):
        print("\n🔹 Searching for categories containing 'Legal' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=0,
            previous_page=0,
        )
        page_result = Page(data=[sample_document_category], meta=pagination)

        mock_repository.find.return_value = page_result

        result = await document_category_service.find(1, 10, "Legal")
        print(f"🔎 Found {len(result.data)} categories with 'Legal'")
        for item in result.data:
            print(f"  - {item.name} (ID: {item.id})")

        mock_repository.find.assert_called_once_with(1, 10, {"name": "Legal"})
        assert isinstance(result, DocumentCategoryPage)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_invalid_page_number(self, document_category_service):
        print("\n🔹 Testing pagination with invalid page number (0) ⚠️")
        with pytest.raises(BadRequestException) as exc:
            await document_category_service.get_paginated_document_categories(0, 10)
        print(f"❌ Error validated correctly: {exc.value.detail}")

    @pytest.mark.asyncio
    async def test_invalid_size_number(self, document_category_service):
        print("\n🔹 Testing pagination with invalid size (0) ⚠️")
        with pytest.raises(BadRequestException) as exc:
            await document_category_service.get_paginated_document_categories(1, 0)
        print(f"❌ Error validated correctly: {exc.value.detail}")
