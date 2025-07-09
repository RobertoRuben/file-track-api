from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.core.db.dependencies import get_async_session
from src.app.domain.department.repository.interface import IDepartmentConnectionRepository
from src.app.domain.department.repository.implementations import DepartmentConnectionRepositoryImpl


async def get_department_connection_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IDepartmentConnectionRepository:
    """
    Dependency function to get the department connection repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of IDepartmentConnectionRepository bound to the provided session
    """
    return DepartmentConnectionRepositoryImpl(session=session)
