from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import IEmployeeRepository
from src.app.repository.implementations import EmployeeRepositoryImpl


async def get_employee_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IEmployeeRepository:
    """
    Dependency function to get the employee repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of IEmployeeRepository bound to the provided session
    """
    return EmployeeRepositoryImpl(session=session)