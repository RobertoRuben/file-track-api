from fastapi import Depends
from src.app.service.interfaces import ISubmitterService
from src.app.service.implementations import SubmitterServiceImpl
from src.app.repository.interfaces import ISubmitterRepository
from src.app.repository.dependencies import get_submitter_repository


async def get_submitter_service(
    repository: ISubmitterRepository = Depends(get_submitter_repository),
) -> ISubmitterService:
    """
    Dependency function to get the submitter service implementation.

    This function creates and provides an instance of the submitter service
    implementation with the necessary repository dependency injected.

    Args:
        repository: The submitter repository implementation provided by
                   the FastAPI dependency injection system.

    Returns:
        An implementation of ISubmitterService configured with the provided repository.
    """
    return SubmitterServiceImpl(repository=repository)
