from fastapi import Depends
from src.app.service.interfaces import IRoleService
from src.app.service.implementations import RoleServiceImpl
from src.app.repository.interfaces import IRoleRepository
from src.app.repository.dependencies import get_role_repository


async def get_role_service(
    repository: IRoleRepository = Depends(get_role_repository),
) -> IRoleService:
    """
    Dependency function to get the role service implementation.

    This function creates and provides an instance of the role service
    implementation with the necessary repository dependency injected.

    :param repository: The role repository implementation provided by
                      the FastAPI dependency injection system
    :return: An implementation of IRoleService configured with the provided repository
    """
    return RoleServiceImpl(repository=repository)
