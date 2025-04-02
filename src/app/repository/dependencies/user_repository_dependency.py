from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.app.db.dependencies import get_async_session
from src.app.repository.interfaces import IUserRepository
from src.app.repository.implementations import UserRepositoryImpl


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> IUserRepository:
    """
    Dependency function to get the user repository implementation.

    Args:
        session: The async database session provided by the FastAPI dependency injection system

    Returns:
        An implementation of IUserRepository bound to the provided session
    """
    return UserRepositoryImpl(session=session)
