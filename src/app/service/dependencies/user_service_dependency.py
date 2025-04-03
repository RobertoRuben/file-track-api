from fastapi import Depends
from src.app.service.interfaces import IUserService
from src.app.service.implementations import UserServiceImpl
from src.app.repository.interfaces import (
    IUserRepository,
    IRolRepository,
    IEmployeeRepository,
)
from src.app.repository.dependencies import (
    get_user_repository,
    get_rol_repository,
    get_employee_repository,
)
from src.app.security.hasher.interface import IHasherProvider
from src.app.security.hasher.dependencies import get_hasher_provider


async def get_user_service(
    user_repository: IUserRepository = Depends(get_user_repository),
    rol_repository: IRolRepository = Depends(get_rol_repository),
    employee_repository: IEmployeeRepository = Depends(get_employee_repository),
    hasher_provider: IHasherProvider = Depends(get_hasher_provider),
) -> IUserService:
    """
    Dependency to get the user service implementation.

    This function creates and provides an instance of the user service implementation
    with the necessary dependencies injected.

    :param user_repository: The user repository implementation provided
                            by FastAPI's dependency injection system.
    :param rol_repository: The role repository implementation provided
                           by FastAPI's dependency injection system.
    :param employee_repository: The employee repository implementation provided
                                by FastAPI's dependency injection system.
    :param hasher_provider: The hash provider implementation provided
                            by FastAPI's dependency injection system.

    :return: An IUserService implementation configured with the provided dependencies.
    """
    return UserServiceImpl(
        user_repository=user_repository,
        rol_repository=rol_repository,
        employee_repository=employee_repository,
        hasher_provider=hasher_provider,
    )
