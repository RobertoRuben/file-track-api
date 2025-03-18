from pydantic import BaseModel
from src.schema import Page

class CategoryDocumentResponseDTO(BaseModel):
    """
    DTO for the response of a document category.
    """
    id: int
    nombre: str


class CategoryDocumentPage(Page):
    """
    DTO for paginated response of document categories.
    """
    items: list[CategoryDocumentResponseDTO]