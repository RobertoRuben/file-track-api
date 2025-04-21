from abc import ABC, abstractmethod
from src.app.dto.response import DocumentResponseDTO


class IReportService(ABC):
    """
    Interfaz para el servicio de generación de reportes.
    Define el contrato para las operaciones relacionadas con la generación de reportes.
    """

    @abstractmethod
    async def generate_document_registration_report(
        self, document_data: DocumentResponseDTO
    ) -> bytes:
        """
        Genera un reporte de registro de documento en formato PDF.

        :param document_data: Los datos del documento para generar el reporte
        :return: El contenido del PDF generado en bytes
        """
        pass
