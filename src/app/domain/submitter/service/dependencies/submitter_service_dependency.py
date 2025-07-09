from fastapi import Depends
from src.app.domain.submitter.service.interface import ISubmitterService
from src.app.domain.submitter.service.implementations import SubmitterServiceImpl
from src.app.domain.submitter.repository.interface import ISubmitterRepository
from src.app.domain.submitter.repository.dependencies import get_submitter_repository


async def get_submitter_service(
    submitter_repository: ISubmitterRepository = Depends(get_submitter_repository),
) -> ISubmitterService:
    """
    Dependency function to get the submitter service implementation.

    This function creates and provides an instance of the submitter service
    implementation with the necessary repository dependency injected.

    :param submitter_repository: The submitter repository implementation provided by
                                the FastAPI dependency injection system
    :return: An implementation of ISubmitterService configured with the provided repository
    """
    return SubmitterServiceImpl(submitter_repository=submitter_repository)
