import os
from src.app.domain.document.dto import DocumentResponseDTO
from src.app.core.exception.decorator.handle_exception import handle_exceptions
from src.app.domain.document.service.interfaces.report_service import IReportService
from src.resources.templates.registration_document_report import create_document_report


class ReportServiceImpl(IReportService):
    """
    Implementación del servicio de reportes usando ReportLab.
    """

    def __init__(self):
        """
        Inicializa el servicio de reportes configurando los recursos necesarios.
        """
        # Rutas para recursos estáticos
        resources_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),
            "resources",
            "static",
        )

        # Ruta para el logo
        self.images_dir = os.path.join(resources_dir, "img")
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

        self.logo_path = os.path.join(self.images_dir, "logo.png")

    @handle_exceptions
    async def generate_document_registration_report(
        self, document_data: DocumentResponseDTO
    ) -> bytes:
        """
        Genera un reporte de registro de documento en formato PDF.

        :param document_data: Los datos del documento para generar el reporte
        :return: El contenido del PDF generado en bytes
        """
        # Usar la plantilla para generar el reporte
        pdf_bytes = create_document_report(
            document_data,
            logo_path=self.logo_path if os.path.exists(self.logo_path) else None,
        )

        return pdf_bytes
