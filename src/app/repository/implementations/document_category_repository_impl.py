import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IDocumentCategoryRepository
from src.app.model.entity import DocumentCategory
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination


class DocumentCategoryRepositoryImpl(IDocumentCategoryRepository):
    """
    Repository implementation for handling DocumentCategory entities.
    Provides methods for CRUD operations and search functionality.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, document_category: DocumentCategory) -> DocumentCategory:
        """
        Save a new document category to the database.

        :param document_category: The DocumentCategory entity to save
        :return: The persisted DocumentCategory with updated attributes
        :raises DatabaseException: If an error occurs during the save operation
        """
        self.session.add(document_category)
        return document_category

    @transactional(readonly=True)
    async def get_all(self) -> list[DocumentCategory]:
        """
        Retrieve all document categories from the database.

        :return: A list of all DocumentCategory entities
        :raises DatabaseException: If an error occurs while retrieving categories
        """
        stmt = select(DocumentCategory)
        results = await self.session.exec(stmt)
        categories = results.all()
        return list(categories)

    @transactional(readonly=False)
    async def delete(self, category_document_id: int) -> bool:
        """
        Delete a document category by its ID.

        :param category_document_id: The ID of the category to delete
        :return: True if the deletion was successful
        :raises DatabaseException: If an error occurs during deletion
        """
        category_document = await self.get_by_id(category_document_id)
        await self.session.delete(category_document)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, category_document_id: int) -> DocumentCategory:
        """
        Retrieve a document category by its ID.

        :param category_document_id: The ID of the category to retrieve
        :return: The DocumentCategory entity with the given ID or None if not found
        :raises DatabaseException: If an error occurs during retrieval
        """
        stmt = select(DocumentCategory).where(
            DocumentCategory.id == category_document_id
        )
        result = await self.session.exec(stmt)
        category_document = result.first()
        return category_document

    @transactional(readonly=True)
    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Retrieve document categories with pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :return: A Page object containing the categories and pagination metadata
        :raises DatabaseException: If an error occurs during the paginated query
        """
        offset_value = (page - 1) * size
        stmt = select(DocumentCategory)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        categories_document = list(results.all())

        count_stmt = select(func.count(DocumentCategory.id))
        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1

        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        pagination_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(data=categories_document, meta=pagination_info)

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for document categories with filtering and pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :param search_dict: Dictionary of field-value pairs to search for
        :return: A Page object containing the filtered categories and pagination metadata
        :raises DatabaseException: If an error occurs during the search operation
        """
        offset_value = (page - 1) * size
        conditions = []

        allowed_fields = ["name"]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name == "name":
                normalized_search = search_value.lower()
                conditions.append(
                    func.lower(DocumentCategory.name).like(f"%{normalized_search}%")
                )

        stmt = select(DocumentCategory)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        categories_document = list(results.all())

        count_stmt = select(func.count(DocumentCategory.id))

        if conditions:
            count_stmt = count_stmt.where(or_(*conditions))

        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()

        total_pages = math.ceil(total_items / size) if total_items > 0 else 1
        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        pagination_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(data=categories_document, meta=pagination_info)

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a document category exists based on the given criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a matching document category exists, False otherwise
        :raises DatabaseException: If an error occurs during the query
        """
        stmt = select(DocumentCategory)
        for field, value in kwargs.items():
            if hasattr(DocumentCategory, field):
                stmt = stmt.where(getattr(DocumentCategory, field) == value)
            else:
                raise InvalidFieldException(f"Invalid field: {field}")

        results = await self.session.exec(stmt)
        category = results.first()
        return category is not None

    @transactional(readonly=False)
    async def delete_by_ids(self, category_ids: list[int]) -> bool:
        """
        Delete multiple document category entities from the database by their IDs.

        :param category_ids: List of document category IDs to delete
        :return: True if the document categories were successfully deleted, False otherwise
        :raises DatabaseException: If an error occurs during deletion
        """    
        stmt = select(DocumentCategory).where(DocumentCategory.id.in_(category_ids))
        results = await self.session.exec(stmt)
        categories = results.all()
        
        found_ids = {category.id for category in categories}
        if len(found_ids) != len(category_ids):
            return False
        for category in categories:
            await self.session.delete(category)
        return True

    @transactional(readonly=True)
    async def find_by_ids(self, category_ids: list[int]) -> list[DocumentCategory]:
        """
        Find multiple document categories by their IDs.

        :param category_ids: List of document category IDs to find
        :return: List of DocumentCategory entities matching the provided IDs
        :raises DatabaseException: If an error occurs during the query
        """
        if not category_ids:
            return []

        stmt = select(DocumentCategory).where(DocumentCategory.id.in_(category_ids))
        results = await self.session.exec(stmt)
        categories = results.all()
        return list(categories)
