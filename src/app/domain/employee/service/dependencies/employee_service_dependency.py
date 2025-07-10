from fastapi import Depends
from src.app.domain.employee.service.interface import IEmployeeService
from src.app.domain.employee.service.implementations import EmployeeServiceImpl
from src.app.domain.employee.repository.interface import (
    IEmployeeRepository,
    IPositionRepository,
)
from src.app.domain.department.repository.interface import IDepartmentRepository
from src.app.domain.employee.repository.dependencies import (
    get_employee_repository,
    get_position_repository,
)
from src.app.domain.department.repository.dependencies import get_department_repository


async def get_employee_service(
    employee_repository: IEmployeeRepository = Depends(get_employee_repository),
    position_repository: IPositionRepository = Depends(get_position_repository),
    department_repository: IDepartmentRepository = Depends(get_department_repository),
) -> IEmployeeService:
    """
    Dependency to obtain the employee service implementation.

    This function creates and provides an instance of the employee service implementation
    with the necessary repository dependencies injected.

    :param employee_repository: Employee repository implementation provided
                              by FastAPI's dependency injection system
    :param position_repository: Position repository implementation provided
                              by FastAPI's dependency injection system
    :param department_repository: Department repository implementation provided
                                by FastAPI's dependency injection system
    :return: An implementation of IEmployeeService configured with the provided repositories
    """
    return EmployeeServiceImpl(
        employee_repository=employee_repository,
        position_repository=position_repository,
        department_repository=department_repository,
    )
