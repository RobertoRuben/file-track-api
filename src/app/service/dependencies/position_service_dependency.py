from fastapi import Depends
from src.app.service.interfaces import IPositionService
from src.app.service.implementations import PositionServiceImpl
from src.app.repository.interfaces import IPositionRepository
from src.app.repository.dependencies import get_position_repository


async def get_position_service(
    position_repository: IPositionRepository = Depends(get_position_repository),
) -> IPositionService:
    """
    Dependency function to get the position service implementation.

    This function creates and provides an instance of the position service
    implementation with the necessary repository dependency injected.

    :param position_repository: The position repository implementation provided by
                                the FastAPI dependency injection system
    :return: An implementation of IPositionService configured with the provided repository
    """
    return PositionServiceImpl(position_repository=position_repository)
