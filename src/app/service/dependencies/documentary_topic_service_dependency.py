from fastapi import Depends
from src.app.service.interfaces import IDocumentaryTopicService
from src.app.service.implementations import DocumentaryTopicServiceImpl
from src.app.repository.interfaces import IDocumentaryTopicRepository
from src.app.repository.dependencies import get_documentary_topic_repository

async def get_documentary_topic_service(repository: IDocumentaryTopicRepository = Depends(get_documentary_topic_repository)) -> IDocumentaryTopicService:
    """
    Dependency function to get the department service implementation.

    This function creates and provides an instance of the department service
    implementation with the necessary repository dependency injected.

    Args:
        repository: The department repository implementation provided by
                    the FastAPI dependency injection system.

    Returns:
        An implementation of IDepartmentService configured with the provided repository.
    """
    return DocumentaryTopicServiceImpl(repository=repository)