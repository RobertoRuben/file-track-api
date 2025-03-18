from pydantic import BaseModel
from datetime import datetime
from src.schema import Page

class CategoryDocumentResponseDTO(BaseModel):
    """
    DTO for the response of a document category.
    """
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime | None = None



class CategoryDocumentPage(Page):
    """
    DTO for paginated response of document categories.
    """
    data: list[CategoryDocumentResponseDTO]