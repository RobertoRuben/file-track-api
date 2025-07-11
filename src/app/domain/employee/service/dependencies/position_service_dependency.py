from fastapi import Depends
from src.app.domain.employee.service.interface import IPositionService
from src.app.domain.employee.service.implementations import PositionServiceImpl
from src.app.domain.employee.repository.interface import IPositionRepository
from src.app.domain.employee.repository.dependencies import get_position_repository


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
