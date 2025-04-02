from fastapi import Depends
from src.app.service.interfaces import IAreaConnectionService
from src.app.service.implementations import AreaConnectionServiceImpl
from src.app.repository.interfaces import IAreaConnectionRepository, IAreaRepository
from src.app.repository.dependencies import (
    get_area_connection_repository,
    get_area_repository,
)


async def get_area_connection_service(
    repository: IAreaConnectionRepository = Depends(get_area_connection_repository),
    area_repository: IAreaRepository = Depends(get_area_repository),
) -> IAreaConnectionService:
    """
    Dependency function to get the area connection service implementation.

    This function creates and provides an instance of the area connection service
    with the necessary repository dependencies injected.

    Args:
        repository: The area connection repository implementation provided
                   by the FastAPI dependency injection system.
        area_repository: The area repository implementation provided
                         by the FastAPI dependency injection system.

    Returns:
        An implementation of IAreaConnectionService configured with the provided repositories.
    """
    return AreaConnectionServiceImpl(
        repository=repository,
        area_repository=area_repository,
    )
