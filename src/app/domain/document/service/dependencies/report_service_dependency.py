from src.app.domain.document.service.interfaces.report_service import IReportService
from src.app.domain.document.service.implementations.report_service_impl import (
    ReportServiceImpl,
)


async def get_report_service() -> IReportService:
    """
    Función de dependencia para obtener la implementación del servicio de reportes.

    :return: Una implementación de IReportService
    """
    return ReportServiceImpl()
