from fastapi import Depends
from src.app.domain.department.repository.interface import IDepartmentRepository
from src.app.domain.department.repository.dependencies import get_department_repository
from src.app.domain.department.service.interface import IDepartmentService
from src.app.domain.department.service.implementations import DepartmentServiceImpl


async def get_department_service(
    repository: IDepartmentRepository = Depends(get_department_repository),
) -> IDepartmentService:
    """
    Dependency function to get the department service implementation.

    :param repository: The department repository implementation provided by the FastAPI dependency injection system
    :return: An implementation of IDepartmentService configured with the provided repository
    """
    return DepartmentServiceImpl(department_repository=repository)
