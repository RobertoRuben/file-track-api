from fastapi import Depends
from src.app.service.interfaces import ISettlementService
from src.app.service.implementations import SettlementServiceImpl
from src.app.repository.interfaces import ISettlementRepository
from src.app.repository.dependencies import get_settlement_repository


async def get_settlement_service(
    repository: ISettlementRepository = Depends(get_settlement_repository),
) -> ISettlementService:
    """
    Dependency function to get the settlement service implementation.

    This function creates and provides an instance of the settlement service
    implementation with the necessary repository dependency injected.

    Args:
        repository: The settlement repository implementation provided by
                    the FastAPI dependency injection system.

    Returns:
        An implementation of ISettlementService configured with the provided repository.
    """
    return SettlementServiceImpl(repository=repository)
