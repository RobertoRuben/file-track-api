from fastapi import Depends
from src.app.service.interfaces import IUserService
from src.app.service.implementations import UserServiceImpl
from src.app.repository.interfaces import (
    IUserRepository,
    IRoleRepository,
    IEmployeeRepository,
)
from src.app.repository.dependencies import (
    get_user_repository,
    get_role_repository,
    get_employee_repository,
)
from src.app.security.hasher.interface import IHasherProvider
from src.app.security.hasher.dependencies import get_hasher_provider


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
