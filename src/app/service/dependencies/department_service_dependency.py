from fastapi import Depends
from src.app.service.interfaces import IDepartmentService
from src.app.service.implementations import DepartmentServiceImpl
from src.app.repository.interfaces import IDepartmentRepository
from src.app.repository.dependencies import get_department_repository


async def get_department_service(
    repository: IDepartmentRepository = Depends(get_department_repository),
) -> IDepartmentService:
    """
    Dependency function to get the department service implementation.

    :param repository: The department repository implementation provided by the FastAPI dependency injection system
    :return: An implementation of IDepartmentService configured with the provided repository
    """
    return DepartmentServiceImpl(department_repository=repository)
