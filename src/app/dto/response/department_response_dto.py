from datetime import datetime
from pydantic import BaseModel, Field
from src.app.schema import Page

class DepartmentResponseDTO(BaseModel):
    """
    DTO for the response of a department.
    Represents the data structure returned when querying departments.
    """
    id: int = Field(description="ID único del departamento en la institución")
    nombre: str = Field(description="Nombre del departamento de la institución")
    created_at: datetime = Field(description="Fecha y hora de creación del departamento")
    updated_at: datetime | None = Field(default=None, description="Fecha y hora de la última actualización del departamento")


class DepartmentPage(Page):
    """
    DTO for paginated response of departments.
    Represents a paginated collection of department data.
    """
    data: list[DepartmentResponseDTO]