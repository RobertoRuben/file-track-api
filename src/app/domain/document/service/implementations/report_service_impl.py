import os
from src.app.domain.document.dto.response import DocumentResponseDTO
from src.app.core.exception.decorator.handle_exception import handle_exceptions
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
        # Paths for static resources
        resources_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            ),
            "resources",
            "static",
        )

        # Path for images
        self.images_dir = os.path.join(resources_dir, "img")
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

        self.logo_path = os.path.join(self.images_dir, "logo.png")

    @handle_exceptions
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
