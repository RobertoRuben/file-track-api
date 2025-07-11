from fastapi import Depends
from src.app.domain.user.service.interface import IRoleService
from src.app.domain.user.service.implementations import RoleServiceImpl
from src.app.domain.user.repository.interface import IRoleRepository
from src.app.domain.user.repository.dependencies import get_role_repository


async def get_role_service(
    role_repository: IRoleRepository = Depends(get_role_repository),
) -> IRoleService:
    """
    Dependency function to get the role service implementation.

    This function creates and provides an instance of the role service
    implementation with the necessary repository dependency injected.

    :param role_repository: The role repository implementation provided by
                       the FastAPI dependency injection system
    :return: An implementation of IRoleService configured with the provided repository
    """
    return RoleServiceImpl(role_repository=role_repository)
