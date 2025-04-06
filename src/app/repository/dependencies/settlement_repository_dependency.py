from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import ISettlementRepository
from src.app.repository.implementations import SettlementRepositoryImpl


async def get_settlement_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ISettlementRepository:
    """
    Dependency function to get the settlement repository implementation.

    :param session: The async database session provided by FastAPI's dependency injection system
    :return: An implementation of ISettlementRepository bound to the provided session
    """
    return SettlementRepositoryImpl(session=session)
