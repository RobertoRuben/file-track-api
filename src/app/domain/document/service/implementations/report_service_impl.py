import os
from src.app.domain.document.dto.response import DocumentResponseDTO
from src.app.core.exception.decorator.service_handle_exception import service_handle_exceptions
from src.app.domain.document.service.interface.report_service import IReportService
from src.resources.templates.registration_document_report import create_document_report


class ReportServiceImpl(IReportService):
    """
    Implementation of the report service using ReportLab.
    """

    def __init__(self):
        """
        Initializes the report service by configuring the necessary resources.
        """
        current_dir = os.path.dirname(__file__)
        while True:
            if os.path.basename(current_dir) == "src":
                src_dir = current_dir
                break
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                raise RuntimeError(
                    "No se encontró la carpeta 'src' en la jerarquía de carpetas."
                )
            current_dir = parent_dir

        resources_base = os.path.join(src_dir, "resources")
        if not os.path.exists(resources_base):
            os.makedirs(resources_base)

        # Paths for static resources
        resources_dir = os.path.join(resources_base, "static")

        # Path for images
        self.images_dir = os.path.join(resources_dir, "img")
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

        self.logo_path = os.path.join(self.images_dir, "logo.png")

    @service_handle_exceptions
    async def generate_document_registration_report(
        self, document_data: DocumentResponseDTO
    ) -> bytes:
        """
        Generates a document registration report in PDF format.

        :param document_data: The document data to generate the report
        :return: The generated PDF content as bytes
        """
        # Use the create_document_report function to generate the PDF
        pdf_bytes = create_document_report(
            document_data,
            logo_path=self.logo_path if os.path.exists(self.logo_path) else None,
        )

        return pdf_bytes
