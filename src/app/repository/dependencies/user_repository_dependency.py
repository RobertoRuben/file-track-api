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

    This function provides an implementation of the user repository interface
    that can be injected into services or other components that need to
    interact with user data in the database.

    :param session: The async database session provided by FastAPI's dependency injection
    :return: An implementation of IUserRepository bound to the provided session
    """
    return UserRepositoryImpl(session=session)
