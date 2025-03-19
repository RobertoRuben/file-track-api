from fastapi import Depends
from src.service.interfaces import IRoleService
from src.service.implementations import RoleServiceImpl
from src.repository.interfaces import IRolRepository
from src.repository.dependencies import get_rol_repository


async def get_role_service(repository: IRolRepository = Depends(get_rol_repository)) -> IRoleService:
    """
    Dependency function to get the role service implementation.

    This function creates and provides an instance of the role service
    implementation with the necessary repository dependency injected.

    Args:
        repository: The role repository implementation provided by
                   the FastAPI dependency injection system.

    Returns:
        An implementation of IRoleService configured with the provided repository.
    """
    return RoleServiceImpl(repository=repository)