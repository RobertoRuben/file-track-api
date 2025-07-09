from fastapi import Depends
from src.app.core.security.hasher.interface import IHasherProvider
from src.app.core.security.hasher.dependencies import get_hasher_provider
from src.app.domain.user.service.interface import IUserService
from src.app.domain.user.service.implementations import UserServiceImpl
from src.app.domain.user.repository.interface import IUserRepository, IRoleRepository
from src.app.domain.user.repository.dependencies import (
    get_user_repository,
    get_role_repository,
)
from src.app.domain.employee.repository.interface import IEmployeeRepository
from src.app.domain.employee.repository.dependencies import get_employee_repository


async def get_user_service(
    user_repository: IUserRepository = Depends(get_user_repository),
    role_repository: IRoleRepository = Depends(get_role_repository),
    employee_repository: IEmployeeRepository = Depends(get_employee_repository),
    hasher_provider: IHasherProvider = Depends(get_hasher_provider),
) -> IUserService:
    """
    Dependency to get the user service implementation.

    This function creates and provides an instance of the user service implementation
    with the necessary dependencies injected.

    :param user_repository: The user repository implementation
    :param role_repository: The role repository implementation
    :param employee_repository: The employee repository implementation
    :param hasher_provider: The password hashing provider implementation
    :return: An IUserService implementation configured with the provided dependencies
    """
    return UserServiceImpl(
        user_repository=user_repository,
        role_repository=role_repository,
        employee_repository=employee_repository,
        hasher_provider=hasher_provider,
    )
