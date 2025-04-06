from fastapi import Depends
from src.app.service.interfaces import IDocumentaryTopicService
from src.app.service.implementations import DocumentaryTopicServiceImpl
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.repository.dependencies import get_documentary_topic_repository


async def get_documentary_topic_service(
    documentary_topic_repository: IDocumentaryTopicRepository = Depends(
        get_documentary_topic_repository
    ),
) -> IDocumentaryTopicService:
    """
    Dependency function to get the documentary topic service implementation.

    This function creates and provides an instance of the documentary topic service
    implementation with the necessary repository dependency injected.

    :param documentary_topic_repository: The documentary topic repository implementation provided by
                      the FastAPI dependency injection system
    :return: An implementation of IDocumentaryTopicService configured with the provided repository
    """
    return DocumentaryTopicServiceImpl(
        documentary_topic_repository=documentary_topic_repository
    )
