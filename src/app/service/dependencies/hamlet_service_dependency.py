from fastapi import Depends
from src.app.service.interfaces import IHamletService
from src.app.service.implementations import HamletServiceImpl
from src.app.repository.interfaces import IHamletRepository, ISettlementRepository
from src.app.repository.dependencies import (
    get_hamlet_repository,
    get_settlement_repository,
)


async def get_hamlet_service(
    hamlet_repository: IHamletRepository = Depends(get_hamlet_repository),
    settlement_repository: ISettlementRepository = Depends(get_settlement_repository),
) -> IHamletService:
    """
    Dependency function to get the hamlet service implementation.

    This function creates and provides an instance of the hamlet service
    implementation with the necessary repository dependencies injected.

    :param hamlet_repository: The hamlet repository implementation provided by
                          the FastAPI dependency injection system.
    :param settlement_repository: The settlement repository implementation provided by
                              the FastAPI dependency injection system.
    :return: An implementation of IHamletService configured with the provided repositories.
    """
    return HamletServiceImpl(
        hamlet_repository=hamlet_repository,
        settlement_repository=settlement_repository,
    )
