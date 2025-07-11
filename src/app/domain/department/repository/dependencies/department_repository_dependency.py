from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.core.db.dependencies import get_async_session
from src.app.domain.department.repository.interface import IDepartmentRepository
from src.app.domain.department.repository.implementations import (
    DepartmentRepositoryImpl,
)


async def get_department_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IDepartmentRepository:
    """
    Dependency function to get the department repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of IDepartmentRepository bound to the provided session
    """
    return DepartmentRepositoryImpl(session=session)
