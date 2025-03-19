from pydantic import BaseModel, Field
from datetime import datetime
from src.schema import Page

class CategoryDocumentResponseDTO(BaseModel):
    """
    DTO for the response of a document category.
    Represents the data structure returned when querying document categories.
    """
    id: int = Field(description="ID único de la categoría del documento")
    nombre: str = Field(description="Nombre de la categoría del documento")
    created_at: datetime = Field(description="Fecha y hora de creación de la categoría")
    updated_at: datetime | None = Field(default=None, description="Fecha y hora de la última actualización de la categoría")


class CategoryDocumentPage(Page):
    """
    DTO for paginated response of document categories.
    Represents a paginated collection of document category data.
    """
    data: list[CategoryDocumentResponseDTO] = Field(description="Lista de categorías de documentos en la página actual")