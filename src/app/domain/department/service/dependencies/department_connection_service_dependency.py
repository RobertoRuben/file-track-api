from fastapi import Depends

from src.app.domain.department.repository.interface import (
    IDepartmentConnectionRepository,
    IDepartmentRepository,
)
from src.app.domain.department.repository.dependencies import (
    get_department_connection_repository,
    get_department_repository,
)
from src.app.domain.department.service.interface import IDepartmentConnectionService
from src.app.domain.department.service.implementations import (
    DepartmentConnectionServiceImpl,
)


async def get_department_connection_service(
    department_connection_repository: IDepartmentConnectionRepository = Depends(
        get_department_connection_repository
    ),
    department_repository: IDepartmentRepository = Depends(get_department_repository),
) -> IDepartmentConnectionService:
    """
    Dependency function to get the department connection service implementation.

    This function creates and provides an instance of the department connection service
    with the necessary repository dependencies injected.

    :param department_connection_repository: The department connection repository implementation provided by the FastAPI dependency injection system
    :param department_repository: The department repository implementation provided by the FastAPI dependency injection system
    :return: An implementation of IDepartmentConnectionService configured with the provided repositories
    """
    return DepartmentConnectionServiceImpl(
        department_connection_repository=department_connection_repository,
        department_repository=department_repository,
    )
