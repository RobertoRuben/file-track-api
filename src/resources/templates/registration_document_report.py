import asyncio
import aiofiles.os as aio_os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    Frame,
    PageTemplate,
)
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime
from io import BytesIO
import os
from src.app.domain.document.dto.response import DocumentResponseDTO


async def create_document_report(
    document_data: DocumentResponseDTO, logo_path: str | None = None
) -> bytes:
    background_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "resources",
        "static",
        "img",
        "report-background.png",
    )

    background_exists = await aio_os.path.exists(background_path)
    logo_exists = logo_path and await aio_os.path.exists(logo_path)

    def generate_pdf():
        buffer = BytesIO()

        def add_page_background(canvas, doc):
            if background_exists:
                canvas.saveState()
                canvas.setFillAlpha(0.5)
                w, h = A4
                canvas.drawImage(background_path, 0, 0, width=w, height=h, mask="auto")

                gen_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                footer_text = f"Reporte generado el: {gen_time}"
                copyright_text = "© Municipalidad Distrital de Asunción. Todos los derechos reservados"

                canvas.setFont("Helvetica", 8)
                canvas.setFillColor(colors.grey)
                canvas.drawCentredString(w / 2, 1.5 * cm, footer_text)
                canvas.drawCentredString(w / 2, 1.0 * cm, copyright_text)

                canvas.restoreState()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )
        main_frame = Frame(
            doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal"
        )
        background_template = PageTemplate(
            id="bg", frames=[main_frame], onPage=add_page_background
        )
        doc.addPageTemplates([background_template])

        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="CenteredTitle",
                parent=styles["Heading1"],
                alignment=TA_CENTER,
                fontSize=16,
                spaceAfter=8,
            )
        )

        styles.add(
            ParagraphStyle(
                name="SystemText",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                fontSize=11,
                textColor=colors.grey,
                spaceAfter=20,
            )
        )

        styles.add(
            ParagraphStyle(
                name="CenteredSubtitle",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                fontSize=11,
                textColor=colors.black,
                spaceAfter=5,
            )
        )

        styles.add(
            ParagraphStyle(
                name="RegistrationInfo",
                parent=styles["Normal"],
                alignment=TA_LEFT,
                fontSize=10,
                spaceAfter=5,
            )
        )

        styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=styles["Normal"],
                fontSize=9,
                fontName="Helvetica-Bold",
                textColor=colors.black,
                spaceBefore=12,
                spaceAfter=8,
            )
        )

        styles.add(
            ParagraphStyle(
                name="Footer",
                parent=styles["Normal"],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER,
            )
        )

        styles.add(
            ParagraphStyle(
                name="TableCell",
                parent=styles["Normal"],
                fontSize=9,
                alignment=TA_LEFT,
                wordWrap="CJK",
                splitLongWords=True,
                spaceShrinkage=0.05,
                leading=14,
                allowWidows=0,
                allowOrphans=0,
                autoLeading="max",
            )
        )

        styles.add(
            ParagraphStyle(
                name="TableLabel",
                parent=styles["TableCell"],
                fontName="Helvetica-Bold",
                fontSize=9,
            )
        )

        label_width = 1.5 * inch
        content_width = doc.width - label_width - 12
        elements = []

        if logo_exists:
            logo = Image(logo_path, width=1.8 * inch, height=0.9 * inch)
            logo.hAlign = "CENTER"
            elements += [logo, Spacer(1, 0.2 * inch)]

        elements.append(Spacer(1, 0.5 * inch))

        elements += [
            Paragraph("REPORTE DE REGISTRO DE DOCUMENTO", styles["CenteredTitle"]),
            Paragraph("Sistema de Gestión Documental", styles["SystemText"]),
            Paragraph(
                f"Código de registro: <b>{document_data.registration_code}</b>",
                styles["CenteredSubtitle"],
            ),
        ]

        elements.append(Spacer(1, 0.3 * inch))

        elements += [
            Paragraph(
                f"<b>Fecha y Hora de Registro:</b> {document_data.created_at.strftime('%d/%m/%Y %H:%M:%S')}",
                styles["RegistrationInfo"],
            ),
            Paragraph(
                f"<b>Registrado por:</b> {document_data.registered_by_user_name}",
                styles["RegistrationInfo"],
            ),
            Spacer(1, 0.25 * inch),
        ]

        created_at = document_data.created_at.strftime("%d/%m/%Y %H:%M:%S")
        updated_at = (
            document_data.updated_at.strftime("%d/%m/%Y %H:%M:%S")
            if document_data.updated_at
            else "N/A"
        )

        table_style = TableStyle(
            [
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]
        )

        def add_section_header(text):
            elements.append(Paragraph(text, styles["SectionHeader"]))

        def format_cell(text):
            if text is None:
                return Paragraph("N/A", styles["TableCell"])
            return Paragraph(str(text), styles["TableCell"])

        add_section_header("DETALLES DEL DOCUMENTO")
        data = [
            [
                Paragraph("Título", styles["TableLabel"]),
                format_cell(document_data.title),
            ],
            [
                Paragraph("Categoría", styles["TableLabel"]),
                format_cell(document_data.document_category_name),
            ],
            [
                Paragraph("Asunto", styles["TableLabel"]),
                format_cell(document_data.subject),
            ],
            [
                Paragraph("Páginas", styles["TableLabel"]),
                format_cell(document_data.pages),
            ],
        ]
        table = Table(data, colWidths=[label_width, content_width])
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))

        add_section_header("PROVENIENCIA DEL DOCUMENTO")
        data = [
            [
                Paragraph("Asentamiento", styles["TableLabel"]),
                format_cell(document_data.settlement_name),
            ],
            [
                Paragraph("Caserío", styles["TableLabel"]),
                format_cell(document_data.hamlet_name),
            ],
            [
                Paragraph("Tema documental", styles["TableLabel"]),
                format_cell(document_data.documentary_topic_name),
            ],
            [
                Paragraph("Registrado por", styles["TableLabel"]),
                format_cell(document_data.registered_by_user_name),
            ],
        ]
        table = Table(data, colWidths=[label_width, content_width])
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))

        add_section_header("INFORMACIÓN DEL REMITENTE")
        data = [
            [
                Paragraph("DNI", styles["TableLabel"]),
                format_cell(document_data.submitter_dni),
            ],
            [
                Paragraph("Nombre completo", styles["TableLabel"]),
                format_cell(document_data.submitter_names),
            ],
        ]
        table = Table(data, colWidths=[label_width, content_width])
        table.setStyle(table_style)
        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))

        doc.build(elements)
        return buffer.getvalue()

    return await asyncio.to_thread(generate_pdf)
