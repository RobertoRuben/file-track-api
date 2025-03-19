from pydantic import BaseModel, Field
from datetime import datetime
from src.schema import Page

class RoleResponseDTO(BaseModel):
    """
    DTO for the response of a role.
    Represents the data structure returned when querying roles.
    """
    id: int = Field(description="ID único del rol")
    nombre: str = Field(description="Nombre del rol")
    created_at: datetime = Field(description="Fecha y hora de creación del rol")
    updated_at: datetime | None = Field(default=None, description="Fecha y hora de la última actualización del rol")


class RolePage(Page):
    """
    DTO for paginated response of roles.
    Represents a paginated collection of role data.
    """
    data: list[RoleResponseDTO]