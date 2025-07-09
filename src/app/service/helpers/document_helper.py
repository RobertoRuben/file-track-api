from datetime import datetime
import os
import uuid
from src.app.core.exception import ServerException


class DocumentHelper:
    """
    Helper class for document-related operations.
    Provides functionalities such as registration code generation and file storage.
    """

    @staticmethod
    def generate_registration_code(last_registration_code: str = None) -> str:
        """
        Generates a registration code for documents based on the last existing code.

        The code format is: DOC + [numeric sequence] + [current date in DDMMYYYY format]

        Examples:
        - If last_registration_code is None: DOC00000000110102025
        - If last_registration_code is DOC00000000110102025: DOC00000000210102025

        :param last_registration_code: The last registration code used (optional)
        :return: A new registration code
        """
        current_date = datetime.now().strftime("%d%m%Y")

        prefix = "DOC"

        if last_registration_code is None:
            sequence_number = 1
        else:
            numeric_part = last_registration_code[3:-8]
            sequence_number = int(numeric_part) + 1

        formatted_sequence = f"{sequence_number:09d}"
        registration_code = f"{prefix}{formatted_sequence}{current_date}"

        return registration_code

    @staticmethod
    async def save_document_file(
        file_content: bytes, extension: str = "pdf"
    ) -> tuple[str, int]:
        """
        Saves a document file to the storage directory.

        :param file_content: Binary content of the file
        :param extension: File extension (default: pdf)
        :return: Tuple containing (storage_path, file_size)
        """
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
            )
        )
        storage_dir = os.path.join(base_dir, "storage", "docs")
        os.makedirs(storage_dir, exist_ok=True)

        if extension.lower() == "pdf" and not file_content.startswith(b'%PDF-'):
            raise ServerException(
                message="Invalid document format",
                details="The provided content does not appear to be a valid PDF file",
                type_="Document Validation Error",
                code=400,
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.{extension}"

        file_path = os.path.join(storage_dir, filename)

        print(f"Saving file to: {file_path}")

        with open(file_path, "wb") as f:
            f.write(file_content)

        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            raise ServerException(
                message="File storage error",
                details=f"Error saving file to {file_path}",
                type_="Storage Error",
                code=500,
            )

        file_size = len(file_content)

        return file_path, file_size


document_helper = DocumentHelper()
