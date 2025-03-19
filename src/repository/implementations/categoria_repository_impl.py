import math
from sqlmodel import select, func, or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from src.repository.interfaces import ICategoriaDocumentoRepository
from src.model.entity import CategoriaDocumento
from src.exception import DatabaseException, InvalidFieldException
from src.schema import Page, Pagination


class CategoriaRepositoryImpl(ICategoriaDocumentoRepository):
    """
    Repository implementation for handling CategoriaDocumento entities.
    Provides methods for CRUD operations and search functionality.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        Args:
            session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    async def save(self, categoria_documento: CategoriaDocumento) -> CategoriaDocumento:
        """
        Save a new document category to the database.

        Args:
            categoria_documento: The CategoriaDocumento entity to save

        Returns:
            The persisted CategoriaDocumento with updated attributes

        Raises:
            DatabaseException: If an error occurs during the save operation
        """
        try:
            self.session.add(categoria_documento)
            await self.session.commit()
            await self.session.refresh(categoria_documento)
            return categoria_documento
        except IntegrityError as e:
            await self.session.rollback()
            raise DatabaseException(
                message="Data integrity error",
                details=str(e.orig),
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                message="Error saving document category",
                details=str(e),
            )

    async def get_all(self) -> list[CategoriaDocumento]:
        """
        Retrieve all document categories from the database.

        Returns:
            A list of all CategoriaDocumento entities

        Raises:
            DatabaseException: If an error occurs while retrieving categories
        """
        try:
            stmt = select(CategoriaDocumento)
            results = await self.session.exec(stmt)
            categories = results.all()
            return list(categories)
        except DatabaseException as e:
            raise DatabaseException(
                message="Error retrieving all categories",
                details=str(e),
            )

    async def delete(self, category_document_id: int) -> bool:
        """
        Delete a document category by its ID.

        Args:
            category_document_id: The ID of the category to delete

        Returns:
            True if the deletion was successful

        Raises:
            DatabaseException: If an error occurs during deletion
        """
        try:
            category_document = await self.get_by_id(category_document_id)
            await self.session.delete(category_document)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                message="Error deleting document category",
                details=str(e),
            )

    async def get_by_id(self, category_document_id: int) -> CategoriaDocumento:
        """
        Retrieve a document category by its ID.

        Args:
            category_document_id: The ID of the category to retrieve

        Returns:
            The CategoriaDocumento entity with the given ID

        Raises:
            DatabaseException: If an error occurs during retrieval
        """
        try:
            stmt = select(CategoriaDocumento).where(CategoriaDocumento.id == category_document_id)
            result = await self.session.exec(stmt)
            category_document = result.first()
            return category_document
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                message="Error retrieving document category by ID",
                details=str(e),
            )

    async def get_pageable(self, page: int = 1, size: int = 10) -> Page:
        """
        Retrieve document categories with pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page

        Returns:
            A Page object containing the categories and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the paginated query
        """
        try:
            offset_value = (page - 1) * size
            stmt = select(CategoriaDocumento)
            stmt = stmt.offset(offset_value).limit(size)
            results = await self.session.exec(stmt)
            categories_document = list(results.all())

            count_stmt = select(func.count(CategoriaDocumento.id))
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

            return Page(
                data=categories_document,
                meta=pagination_info
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                message="Error retrieving paginated document categories",
                details=str(e),
            )

    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for document categories with filtering and pagination.

        Args:
            page: The page number (1-based indexing)
            size: The number of items per page
            search_dict: Dictionary of field-value pairs to search for

        Returns:
            A Page object containing the filtered categories and pagination metadata

        Raises:
            DatabaseException: If an error occurs during the search operation
        """
        try:
            offset_value = (page - 1) * size
            conditions = []

            allowed_fields = ["nombre"]

            for field_name, search_value in search_dict.items():
                if not search_value or field_name not in allowed_fields:
                    continue

                if field_name == "nombre":
                    normalized_search = search_value.lower()
                    conditions.append(func.lower(CategoriaDocumento.nombre).like(f"%{normalized_search}%"))

            stmt = select(CategoriaDocumento)

            if conditions:
                stmt = stmt.where(or_(*conditions))

            stmt = stmt.offset(offset_value).limit(size)
            results = await self.session.exec(stmt)
            categories_document = list(results.all())

            count_stmt = select(func.count(CategoriaDocumento.id))

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

            return Page(
                data=categories_document,
                meta=pagination_info
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                message="Error searching document categories",
                details=str(e),
            )

    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a document category exists based on the provided criteria.

        Args:
            **kwargs: Field-value pairs to check against

        Returns:
            True if a matching category exists, False otherwise

        Raises:
            InvalidFieldException: If an invalid field name is provided
            DatabaseException: If an error occurs during the query
        """
        try:
            valid_fields = CategoriaDocumento.__dict__.keys()
            for key in kwargs.keys():
                if key not in valid_fields:
                    raise InvalidFieldException(
                        message=f"Field '{key}' does not exist in the CategoriaDocumento model",
                        details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}"
                    )

            stmt = select(CategoriaDocumento.id)
            for key, value in kwargs.items():
                stmt = stmt.where(getattr(CategoriaDocumento, key) == value)

            result = await self.session.exec(stmt)
            return result.first() is not None
        except InvalidFieldException as e:
            raise e
        except AttributeError as e:
            await self.session.rollback()
            raise InvalidFieldException(
                message="Error in provided attributes",
                details=str(e)
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseException(
                message="Error checking document category existence",
                details=str(e),
            )