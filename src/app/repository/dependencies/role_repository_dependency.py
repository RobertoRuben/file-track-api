from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.core.db.dependencies import get_async_session
from src.app.repository.interfaces import IRoleRepository
from src.app.repository.implementations import RoleRepositoryImpl


async def get_role_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IRoleRepository:
    """
    Dependency function to get the role repository implementation.

    :param session: The async database session provided by the FastAPI dependency injection system
    :return: An implementation of IRoleRepository bound to the provided session
    """
    return RoleRepositoryImpl(session=session)
