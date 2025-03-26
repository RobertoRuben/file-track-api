from fastapi import Depends
from src.app.service.interfaces import IEmployeeService
from src.app.service.implementations import EmployeeServiceImpl
from src.app.repository.interfaces import (
    IEmployeeRepository,
    IPositionRepository,
    IAreaRepository,
)
from src.app.repository.dependencies import (
    get_employee_repository,
    get_position_repository,
    get_area_repository,
)


async def get_employee_service(
    employee_repository: IEmployeeRepository = Depends(get_employee_repository),
    position_repository: IPositionRepository = Depends(get_position_repository),
    area_repository: IAreaRepository = Depends(get_area_repository),
) -> IEmployeeService:
    """
    Dependencia para obtener la implementación del servicio de empleados.

    Esta función crea y proporciona una instancia de la implementación del servicio
    de empleados con las dependencias de repositorios necesarias inyectadas.

    Args:
        employee_repository: Implementación del repositorio de empleados proporcionada
                            por el sistema de inyección de dependencias de FastAPI.
        position_repository: Implementación del repositorio de cargos proporcionada
                            por el sistema de inyección de dependencias de FastAPI.
        area_repository: Implementación del repositorio de áreas proporcionada
                        por el sistema de inyección de dependencias de FastAPI.

    Returns:
        Una implementación de IEmployeeService configurada con los repositorios proporcionados.
    """
    return EmployeeServiceImpl(
        employee_repository=employee_repository,
        position_repository=position_repository,
        area_repository=area_repository,
    )
