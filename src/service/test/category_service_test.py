import pytest
from unittest.mock import AsyncMock
from datetime import datetime
import pytest_asyncio

from src.model.entity import CategoriaDocumento
from src.dto.request import CategoryDocumentRequestDTO
from src.dto.response import CategoryDocumentResponseDTO, CategoryDocumentPage
from src.schema import MessageResponse, Pagination, Page
from src.exception import ConflictException, NotFoundException, BadRequestException
from src.service.implementations import CategoryDocumentServiceImpl


@pytest.fixture
def mock_repository():
    repository = AsyncMock()
    return repository


@pytest_asyncio.fixture
async def category_document_service(mock_repository):
    return CategoryDocumentServiceImpl(repository=mock_repository)


@pytest.fixture
def sample_category_document():
    return CategoriaDocumento(
        id=1,
        nombre="Documentos Legales",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_request_dto():
    return CategoryDocumentRequestDTO(
        nombre="Documentos Legales"
    )


class TestCategoryDocumentServiceImpl:

    @pytest.mark.asyncio
    async def test_add_category_document_success(self, category_document_service, mock_repository,
                                                 sample_category_document, sample_request_dto):
        print(f"\n🔹 Creando nueva categoría de documento: '{sample_request_dto.nombre}' 🔹")
        mock_repository.exists_by.return_value = False
        mock_repository.save.return_value = sample_category_document

        result = await category_document_service.add_category_document(sample_request_dto)
        print(f"✅ Categoría creada exitosamente con ID: {result.id}")

        mock_repository.exists_by.assert_called_once_with(nombre=sample_request_dto.nombre)
        mock_repository.save.assert_called_once()
        assert isinstance(result, CategoryDocumentResponseDTO)
        assert result.id == sample_category_document.id
        assert result.nombre == sample_category_document.nombre

    @pytest.mark.asyncio
    async def test_add_category_document_conflict(self, category_document_service, mock_repository, sample_request_dto):
        print(f"\n🔹 Intentando crear categoría duplicada: '{sample_request_dto.nombre}' 🔹")
        mock_repository.exists_by.return_value = True

        with pytest.raises(ConflictException) as exc:
            await category_document_service.add_category_document(sample_request_dto)
        print(f"⚠️ Conflicto detectado: {exc.value.detail}")

        mock_repository.save.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_all_categories_documents(self, category_document_service, mock_repository,
                                                sample_category_document):
        print("\n🔹 Obteniendo todas las categorías de documentos 🔍")
        mock_repository.get_all.return_value = [sample_category_document]

        result = await category_document_service.get_all_categories_documents()
        print(f"📋 Se encontraron {len(result)} categorías")

        mock_repository.get_all.assert_called_once()
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], CategoryDocumentResponseDTO)
        assert result[0].id == sample_category_document.id

    @pytest.mark.asyncio
    async def test_update_category_document_same_name(self, category_document_service, mock_repository,
                                                      sample_category_document, sample_request_dto):
        print(f"\n🔹 Actualizando categoría ID: 1 manteniendo nombre: '{sample_request_dto.nombre}' 🔄")
        mock_repository.exists_by.return_value = True  # Solo verifica ID
        mock_repository.get_by_id.return_value = sample_category_document
        mock_repository.save.return_value = sample_category_document

        result = await category_document_service.update_category_document(1, sample_request_dto)
        print(f"✅ Categoría actualizada exitosamente: {result.nombre}")

        assert mock_repository.exists_by.call_count == 1  # Solo una llamada para verificar ID
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.save.assert_called_once()
        assert isinstance(result, CategoryDocumentResponseDTO)

    @pytest.mark.asyncio
    async def test_update_category_document_different_name(self, category_document_service, mock_repository,
                                                           sample_category_document):
        different_name_dto = CategoryDocumentRequestDTO(nombre="Documentos Financieros")

        print(
            f"\n🔹 Cambiando nombre de categoría ID: 1 de '{sample_category_document.nombre}' a '{different_name_dto.nombre}' 🔄")

        mock_repository.exists_by.side_effect = [True, False]  # Primero verifica ID, luego nombre
        mock_repository.get_by_id.return_value = sample_category_document

        updated_document = CategoriaDocumento(
            id=1,
            nombre="Documentos Financieros",
            created_at=sample_category_document.created_at,
            updated_at=datetime.now()
        )
        mock_repository.save.return_value = updated_document

        result = await category_document_service.update_category_document(1, different_name_dto)
        print(f"✅ Nombre cambiado exitosamente: '{result.nombre}'")

        assert mock_repository.exists_by.call_count == 2
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.save.assert_called_once()
        assert isinstance(result, CategoryDocumentResponseDTO)
        assert result.nombre == "Documentos Financieros"

    @pytest.mark.asyncio
    async def test_update_category_document_not_found(self, category_document_service, mock_repository,
                                                      sample_request_dto):
        print(f"\n🔹 Intentando actualizar categoría inexistente (ID: 999) 🔄")
        mock_repository.exists_by.return_value = False

        with pytest.raises(NotFoundException) as exc:
            await category_document_service.update_category_document(999, sample_request_dto)
        print(f"⚠️ Error: {exc.value.detail}")

    @pytest.mark.asyncio
    async def test_delete_category_document_success(self, category_document_service, mock_repository):
        print("\n🔹 Eliminando categoría de documento (ID: 1) 🗑️")
        mock_repository.exists_by.return_value = True
        mock_repository.delete.return_value = True

        result = await category_document_service.delete_category_document(1)
        print(f"✅ {result.message} - {result.details}")

        mock_repository.exists_by.assert_called_once_with(id=1)
        mock_repository.delete.assert_called_once_with(1)
        assert isinstance(result, MessageResponse)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_get_category_document_by_id_success(self, category_document_service, mock_repository,
                                                       sample_category_document):
        print("\n🔹 Buscando categoría de documento por ID: 1 🔍")
        mock_repository.exists_by.return_value = True
        mock_repository.get_by_id.return_value = sample_category_document

        result = await category_document_service.get_category_document_by_id(1)
        print(f"✅ Categoría encontrada: '{result.nombre}'")

        mock_repository.exists_by.assert_called_once_with(id=1)
        mock_repository.get_by_id.assert_called_once_with(1)
        assert isinstance(result, CategoryDocumentResponseDTO)
        assert result.id == sample_category_document.id

    @pytest.mark.asyncio
    async def test_get_paginated_category_documents(self, category_document_service, mock_repository,
                                                    sample_category_document):
        print("\n🔹 Obteniendo categorías de documentos con paginación (página: 1, tamaño: 10) 📄")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=0,
            previous_page=0
        )
        page_result = Page(
            data=[sample_category_document],
            meta=pagination
        )

        mock_repository.get_pageable.return_value = page_result

        result = await category_document_service.get_paginated_category_documents(1, 10)
        print(
            f"📋 Página {result.meta.current_page} de {result.meta.total_pages}, {len(result.data)} resultados de {result.meta.total} en total")

        mock_repository.get_pageable.assert_called_once_with(1, 10)
        assert isinstance(result, CategoryDocumentPage)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_find_success(self, category_document_service, mock_repository, sample_category_document):
        print("\n🔹 Buscando categorías que contengan 'Legal' 🔍")
        pagination = Pagination(
            current_page=1,
            per_page=10,
            total=1,
            total_pages=1,
            next_page=0,
            previous_page=0
        )
        page_result = Page(
            data=[sample_category_document],
            meta=pagination
        )

        mock_repository.find.return_value = page_result

        result = await category_document_service.find(1, 10, "Legal")
        print(f"🔎 Se encontraron {len(result.data)} categorías con 'Legal'")
        for item in result.data:
            print(f"  - {item.nombre} (ID: {item.id})")

        mock_repository.find.assert_called_once_with(1, 10, {"nombre": "Legal"})
        assert isinstance(result, CategoryDocumentPage)
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_invalid_page_number(self, category_document_service):
        print("\n🔹 Probando paginación con número de página inválido (0) ⚠️")
        with pytest.raises(BadRequestException) as exc:
            await category_document_service.get_paginated_category_documents(0, 10)
        print(f"❌ Error validado correctamente: {exc.value.detail}")

    @pytest.mark.asyncio
    async def test_invalid_size_number(self, category_document_service):
        print("\n🔹 Probando paginación con tamaño inválido (0) ⚠️")
        with pytest.raises(BadRequestException) as exc:
            await category_document_service.get_paginated_category_documents(1, 0)
        print(f"❌ Error validado correctamente: {exc.value.detail}")