import math
from datetime import date
from typing import Any

from sqlmodel import select, func, or_, and_, cast, String
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IDocumentRepository
from src.app.model.entity import (
    Document,
    Submitter,
    DocumentCategory,
    DocumentaryTopic,
    Hamlet,
    Settlement,
    User,
)
from src.app.exception.invalid_field_exception import InvalidFieldException
from src.app.schema import Page, Pagination


class DocumentRepositoryImpl(IDocumentRepository):
    """
    Repository implementation for handling Document entities.
    Provides methods for CRUD operations and search functionality for documents.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, document: Document) -> Document:
        """
        Save a document to the database.

        :param document: The document to save
        :return: The saved document with updated data
        """
        self.session.add(document)
        return document

    @transactional(readonly=True)
    async def get_all(self) -> list[Document]:
        """
        Retrieve all documents from the database.

        :return: A list containing all documents
        """
        stmt = select(Document)
        results = await self.session.exec(stmt)
        documents = results.all()
        return list(documents)

    @transactional(readonly=False)
    async def delete(self, document_id: int) -> bool:
        """
        Delete a document by its ID.

        :param document_id: The ID of the document to delete
        :return: True if the document was successfully deleted, False otherwise
        """
        document = await self.get_by_id(document_id)
        await self.session.delete(document)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, document_id: int) -> Document:
        """
        Retrieve a document by its ID.

        :param document_id: The ID of the document to retrieve
        :return: The found document
        """
        stmt = select(Document).where(Document.id == document_id)
        results = await self.session.exec(stmt)
        document = results.first()
        return document

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of documents with related entity information.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing documents and pagination information
        """
        offset = (page - 1) * size

        stmt = (
            select(
                Document.id,
                Document.registration_code,
                Document.title,
                Document.subject,
                Document.pages,
                Document.storage_path,
                Document.size,
                Document.submitter_id,
                Submitter.dni.label("submitter_dni"),
                Document.document_category_id,
                DocumentCategory.name.label("document_category_name"),
                Document.documentary_topic_id,
                DocumentaryTopic.name.label("documentary_topic_name"),
                Document.hamlet_id,
                Hamlet.name.label("hamlet_name"),
                Document.settlement_id,
                Settlement.name.label("settlement_name"),
                Document.registered_by_user_id,
                User.username.label("registered_by_username"),
                Document.created_at,
                Document.updated_at,
            )
            .join(Submitter, Submitter.id == Document.submitter_id)
            .join(
                DocumentCategory, DocumentCategory.id == Document.document_category_id
            )
            .join(
                DocumentaryTopic, DocumentaryTopic.id == Document.documentary_topic_id
            )
            .outerjoin(Hamlet, Hamlet.id == Document.hamlet_id)
            .join(Settlement, Settlement.id == Document.settlement_id)
            .join(User, User.id == Document.registered_by_user_id)
        )

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        documents_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Document.id))
        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1

        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        page_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(
            data=documents_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Search for documents according to search criteria with pagination.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary containing search parameters
        :return: A Page object with documents that match the search criteria
        """
        offset = (page - 1) * size
        conditions = []

        allowed_fields = [
            "registration_code",
            "title",
            "subject",
            "submitter_id",
            "document_category_id",
            "documentary_topic_id",
            "hamlet_id",
            "settlement_id",
            "registered_by_user_id",
            "submitter_dni",
        ]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name in [
                "submitter_id",
                "document_category_id",
                "documentary_topic_id",
                "hamlet_id",
                "settlement_id",
                "registered_by_user_id",
            ]:
                try:
                    value = int(search_value)
                    conditions.append(getattr(Document, field_name) == value)
                except ValueError:
                    pass
            elif field_name == "submitter_dni":
                dni_value = search_value
                conditions.append(cast(Submitter.dni, String) == dni_value)
                conditions.append(cast(Submitter.dni, String).like(f"%{dni_value}%"))
            elif field_name in ["registration_code", "title", "subject"]:
                normalized_search = search_value.lower()
                field = getattr(Document, field_name)
                conditions.append(func.lower(field).like(f"%{normalized_search}%"))

        stmt = (
            select(
                Document.id,
                Document.registration_code,
                Document.title,
                Document.subject,
                Document.pages,
                Document.storage_path,
                Document.size,
                Document.submitter_id,
                Submitter.dni.label("submitter_dni"),
                Document.document_category_id,
                DocumentCategory.name.label("document_category_name"),
                Document.documentary_topic_id,
                DocumentaryTopic.name.label("documentary_topic_name"),
                Document.hamlet_id,
                Hamlet.name.label("hamlet_name"),
                Document.settlement_id,
                Settlement.name.label("settlement_name"),
                Document.registered_by_user_id,
                User.username.label("registered_by_username"),
                Document.created_at,
                Document.updated_at,
            )
            .join(Submitter, Submitter.id == Document.submitter_id)
            .join(
                DocumentCategory, DocumentCategory.id == Document.document_category_id
            )
            .join(
                DocumentaryTopic, DocumentaryTopic.id == Document.documentary_topic_id
            )
            .outerjoin(Hamlet, Hamlet.id == Document.hamlet_id)
            .join(Settlement, Settlement.id == Document.settlement_id)
            .join(User, User.id == Document.registered_by_user_id)
        )

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        documents_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Document.id)).join(
            Submitter, Submitter.id == Document.submitter_id
        )

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
            data=documents_data,
            meta=pagination_info,
        )

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a document exists based on the provided criteria.

        :param kwargs: Key-value pairs representing the search criteria
        :return: True if a document matching the criteria exists, False otherwise
        """
        valid_fields = Document.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the Document model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(Document.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(Document, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None

    @transactional(readonly=True)
    async def get_by_registration_code(self, registration_code: str) -> Document:
        """
        Retrieve a document by its registration code.

        :param registration_code: The registration code of the document to retrieve
        :return: The found document
        """
        stmt = select(Document).where(Document.registration_code == registration_code)
        results = await self.session.exec(stmt)
        document = results.first()
        return document

    @transactional(readonly=True)
    async def find_by_current_date(
        self,
        page: int,
        size: int,
        search_dict: dict[str, str],
    ) -> Page:
        """
        Search for documents created on the current date with additional search criteria.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :param search_dict: Dictionary with search parameters
        :return: A Page object with documents that match the search criteria
        """
        offset = (page - 1) * size
        conditions = []

        today = date.today()
        conditions.append(func.date(Document.created_at) == today)

        allowed_fields = [
            "registration_code",
            "title",
            "subject",
            "submitter_id",
            "document_category_id",
            "documentary_topic_id",
            "hamlet_id",
            "settlement_id",
            "registered_by_user_id",
            "submitter_dni",
        ]

        for field_name, search_value in search_dict.items():
            if not search_value or field_name not in allowed_fields:
                continue

            if field_name in [
                "submitter_id",
                "document_category_id",
                "documentary_topic_id",
                "hamlet_id",
                "settlement_id",
                "registered_by_user_id",
            ]:
                try:
                    value = int(search_value)
                    conditions.append(getattr(Document, field_name) == value)
                except ValueError:
                    pass
            elif field_name == "submitter_dni":
                dni_value = search_value
                conditions.append(cast(Submitter.dni, String) == dni_value)
                conditions.append(cast(Submitter.dni, String).like(f"%{dni_value}%"))
            elif field_name in ["registration_code", "title", "subject"]:
                normalized_search = search_value.lower()
                field = getattr(Document, field_name)
                conditions.append(func.lower(field).like(f"%{normalized_search}%"))

        stmt = (
            select(
                Document.id,
                Document.registration_code,
                Document.title,
                Document.subject,
                Document.pages,
                Document.storage_path,
                Document.size,
                Document.submitter_id,
                Submitter.dni.label("submitter_dni"),
                Document.document_category_id,
                DocumentCategory.name.label("document_category_name"),
                Document.documentary_topic_id,
                DocumentaryTopic.name.label("documentary_topic_name"),
                Document.hamlet_id,
                Hamlet.name.label("hamlet_name"),
                Document.settlement_id,
                Settlement.name.label("settlement_name"),
                Document.registered_by_user_id,
                User.username.label("registered_by_username"),
                Document.created_at,
                Document.updated_at,
            )
            .join(Submitter, Submitter.id == Document.submitter_id)
            .join(
                DocumentCategory, DocumentCategory.id == Document.document_category_id
            )
            .join(
                DocumentaryTopic, DocumentaryTopic.id == Document.documentary_topic_id
            )
            .outerjoin(Hamlet, Hamlet.id == Document.hamlet_id)
            .join(Settlement, Settlement.id == Document.settlement_id)
            .join(User, User.id == Document.registered_by_user_id)
            .where(and_(*conditions))
        )

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        documents_data = [dict(row._mapping) for row in results]

        count_stmt = (
            select(func.count(Document.id))
            .join(Submitter, Submitter.id == Document.submitter_id)
            .where(and_(*conditions))
        )

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
            data=documents_data,
            meta=pagination_info,
        )

    @transactional(readonly=True)
    async def get_last_registration_code(self) -> str | None:
        """
        Retrieve the last registration code from the documents.
        This method is useful for generating new registration codes.
        :return: last registration code or None if no documents exist
        """
        stmt = (
            select(Document.registration_code)
            .order_by(Document.created_at.desc())
            .limit(1)
        )

        result = await self.session.exec(stmt)
        last_registration_code = result.first()
        return last_registration_code

    @transactional(readonly=True)
    async def get_pageable_by_current_date(self, page: int, size: int) -> Page:
        """
        Retrieve a paginated list of documents created on the current date with related entity information.

        :param page: The page number (starts at 1)
        :param size: The size of each page
        :return: A Page object containing documents created today and pagination information
        """
        offset = (page - 1) * size
        today = date.today()

        stmt = (
            select(
                Document.id,
                Document.registration_code,
                Document.title,
                Document.subject,
                Document.pages,
                Document.storage_path,
                Document.size,
                Document.submitter_id,
                Submitter.dni.label("submitter_dni"),
                Document.document_category_id,
                DocumentCategory.name.label("document_category_name"),
                Document.documentary_topic_id,
                DocumentaryTopic.name.label("documentary_topic_name"),
                Document.hamlet_id,
                Hamlet.name.label("hamlet_name"),
                Document.settlement_id,
                Settlement.name.label("settlement_name"),
                Document.registered_by_user_id,
                User.username.label("registered_by_username"),
                Document.created_at,
                Document.updated_at,
            )
            .join(Submitter, Submitter.id == Document.submitter_id)
            .join(
                DocumentCategory, DocumentCategory.id == Document.document_category_id
            )
            .join(
                DocumentaryTopic, DocumentaryTopic.id == Document.documentary_topic_id
            )
            .outerjoin(Hamlet, Hamlet.id == Document.hamlet_id)
            .join(Settlement, Settlement.id == Document.settlement_id)
            .join(User, User.id == Document.registered_by_user_id)
            .where(func.date(Document.created_at) == today)
        )

        stmt = stmt.offset(offset).limit(size)
        results = await self.session.exec(stmt)
        documents_data = [dict(row._mapping) for row in results]

        count_stmt = select(func.count(Document.id)).where(
            func.date(Document.created_at) == today
        )
        count_result = await self.session.exec(count_stmt)
        total_items = count_result.first()

        total_pages = math.ceil(total_items / size) if total_items > 0 else 1
        next_page = page + 1 if page < total_pages else None
        previous_page = page - 1 if page > 1 else None

        page_info = Pagination(
            current_page=page,
            per_page=size,
            total=total_items,
            total_pages=total_pages,
            next_page=next_page,
            previous_page=previous_page,
        )

        return Page(
            data=documents_data,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def get_document_information_by_id(
        self, document_id: int
    ) -> dict[str, Any] | None:
        stmt = select(
            Document.id,
            Document.registration_code,
            Document.title,
            Document.subject,
            Document.pages,
            DocumentaryTopic.name.label("documentary_topic_name"),
            DocumentCategory.name.label("document_category_name"),
            Settlement.name.label("settlement_name"),
            Hamlet.name.label("hamlet_name"),
            Submitter.dni.label("submitter_dni"),
            func.concat(
                Submitter.paternal_surname,
                ' ',
                Submitter.maternal_surname,
                ' ',
                Submitter.names,
            ).label("submitter_names"),
            User.username.label("registered_by_username"),
            Document.created_at,
        ).where(Document.id == document_id)
        results = await self.session.exec(stmt)
        document_info = results.first()

        return document_info._asdict() if document_info else None
