from fastapi import Depends
from src.app.service.interfaces import IDepartmentService
from src.app.service.implementations import DepartmentServiceImpl
from src.app.repository.interfaces import IAreaRepository
from src.app.repository.dependencies import get_area_repository

async def get_department_service(repository: IAreaRepository = Depends(get_area_repository)) -> IDepartmentService:
    """
    Dependency function to get the department service implementation.

    This function creates and provides an instance of the department service
    implementation with the necessary repository dependency injected.

    Args:
        repository: The department repository implementation provided by
                    the FastAPI dependency injection system.

    Returns:
        An implementation of IDepartmentService configured with the provided repository.
    """
    return DepartmentServiceImpl(repository=repository)