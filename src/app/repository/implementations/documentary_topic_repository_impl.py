import math
from sqlmodel import select, func, or_
from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.repository.decorator import transactional
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.model.entity import DocumentaryTopic
from src.app.exception import InvalidFieldException
from src.app.schema import Page, Pagination


class DocumentaryTopicRepositoryImpl(IDocumentaryTopicRepository):

    def __init__(self, session: AsyncSession):
        """
        Initialize the repository with a database session.

        :param session: The SQLAlchemy AsyncSession instance for database operations
        """
        self.session = session

    @transactional(readonly=False)
    async def save(self, documentary_topic: DocumentaryTopic) -> DocumentaryTopic:
        """
        Save a documentary topic entity to the database.

        :param documentary_topic: The documentary topic entity to save
        :return: The persisted documentary topic with updated attributes
        """
        self.session.add(documentary_topic)
        return documentary_topic

    @transactional(readonly=True)
    async def get_all(self) -> list[DocumentaryTopic]:
        """
        Retrieve all documentary topic entities from the database.

        :return: A list of all documentary topic entities
        """
        stmt = select(DocumentaryTopic)
        results = await self.session.exec(stmt)
        documentary_topics = results.all()
        return list(documentary_topics)

    @transactional(readonly=False)
    async def delete(self, documentary_topic_id: int) -> bool:
        """
        Delete a documentary topic entity by its ID.

        :param documentary_topic_id: The ID of the documentary topic to delete
        :return: True if the deletion was successful
        """
        documentary_topic = await self.get_by_id(documentary_topic_id)
        await self.session.delete(documentary_topic)
        return True

    @transactional(readonly=True)
    async def get_by_id(self, documentary_topic_id: int) -> DocumentaryTopic:
        """
        Retrieve a documentary topic entity by its ID.

        :param documentary_topic_id: The ID of the documentary topic to retrieve
        :return: The documentary topic entity with the given ID
        """
        stmt = select(DocumentaryTopic).where(
            DocumentaryTopic.id == documentary_topic_id
        )
        results = await self.session.exec(stmt)
        documentary_topic = results.first()
        return documentary_topic

    @transactional(readonly=True)
    async def get_pageable(self, page: int, size: int) -> Page:
        """
        Retrieve documentary topics with pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :return: A Page object containing the documentary topics and pagination metadata
        """
        offset_value = (page - 1) * size
        stmt = select(DocumentaryTopic)
        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        documentary_topics = list(results.all())

        count_stmt = select(func.count(DocumentaryTopic.id))
        count_results = await self.session.exec(count_stmt)
        total_items = count_results.first()
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
            data=documentary_topics,
            meta=page_info,
        )

    @transactional(readonly=True)
    async def find(self, page: int, size: int, search_dict: dict[str, str]) -> Page:
        """
        Search for documentary topics with filtering and pagination.

        :param page: The page number (1-based indexing)
        :param size: The number of items per page
        :param search_dict: Dictionary of field-value pairs to search for
        :return: A Page object containing the filtered documentary topics and pagination metadata
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
                    func.lower(DocumentaryTopic.name).like(f"%{normalized_search}%")
                )

        stmt = select(DocumentaryTopic)

        if conditions:
            stmt = stmt.where(or_(*conditions))

        stmt = stmt.offset(offset_value).limit(size)
        results = await self.session.exec(stmt)
        documentary_topics = list(results.all())

        count_stmt = select(func.count(DocumentaryTopic.id))

        if conditions:
            count_stmt = count_stmt.where(or_(*conditions))

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

        return Page(data=documentary_topics, meta=page_info)

    @transactional(readonly=True)
    async def exists_by(self, **kwargs) -> bool:
        """
        Check if a documentary topic exists based on the provided criteria.

        :param kwargs: Field-value pairs to check against
        :return: True if a matching documentary topic exists, False otherwise
        :raises InvalidFieldException: If an invalid field name is provided
        """
        valid_fields = DocumentaryTopic.__dict__.keys()
        for key in kwargs.keys():
            if key not in valid_fields:
                raise InvalidFieldException(
                    message=f"Field '{key}' does not exist in the DocumentaryTopic model",
                    details=f"Valid fields are: {', '.join([f for f in valid_fields if not f.startswith('_')])}",
                )

        stmt = select(DocumentaryTopic.id)
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(DocumentaryTopic, key) == value)

        result = await self.session.exec(stmt)
        return result.first() is not None
    
    @transactional(readonly=False)
    async def delete_by_ids(self, documentary_topic_ids: list[int]) -> bool:
        """
        Delete documentary topics by their IDs.

        :param documentary_topic_ids: List of IDs of the documentary topics to delete
        :return: True if the topics were successfully deleted, False otherwise
        """
        if not documentary_topic_ids:
            return False

        stmt = select(DocumentaryTopic).where(
            DocumentaryTopic.id.in_(documentary_topic_ids)
        )
        results = await self.session.exec(stmt)
        documentary_topics = results.all()
        
        founds_ids = {topics.id for topics in documentary_topics}
        if len(founds_ids) != len(documentary_topic_ids):
            return False
        for topic in documentary_topics:
            await self.session.delete(topic)
        return True
    
    @transactional(readonly=True)
    async def find_by_ids(self, documentary_topic_ids: list[int]) -> list[DocumentaryTopic]:
        """
        Find documentary topics by their IDs.

        :param documentary_topic_ids: List of IDs of the documentary topics to find
        :return: A list of documentary topics matching the provided IDs
        """
        if not documentary_topic_ids:
            return []

        stmt = select(DocumentaryTopic).where(
            DocumentaryTopic.id.in_(documentary_topic_ids)
        )
        results = await self.session.exec(stmt)
        documentary_topics = results.all()
        return list(documentary_topics)
    
