from fastapi import Depends
from src.app.domain.location.service.interface import ISettlementService
from src.app.domain.location.service.implementations import SettlementServiceImpl
from src.app.domain.location.repository.interface import ISettlementRepository
from src.app.domain.location.repository.dependencies import get_settlement_repository


async def get_settlement_service(
    settlement_repository: ISettlementRepository = Depends(get_settlement_repository),
) -> ISettlementService:
    """
    Dependency function to get the settlement service implementation.

    This function creates and provides an instance of the settlement service
    implementation with the necessary repository dependency injected.

    :param settlement_repository: The settlement repository implementation provided by
                       the FastAPI dependency injection system
    :return: An implementation of ISettlementService configured with the provided repository
    """
    return SettlementServiceImpl(settlement_repository=settlement_repository)
