from datetime import datetime
from pydantic import BaseModel, Field
from src.app.schema import Page


class PositionResponseDTO(BaseModel):
    """
    DTO for position response.
    Represents the data structure returned when querying positions.
    """

    id: int = Field(
        description="Unique position ID",
        examples=[1, 2, 3]
    )
    nombre: str = Field(
        description="Position name",
        examples=["Project Manager", "Developer", "Designer"]
    )
    created_at: datetime = Field(
        description="Creation date and time of the position",
        examples=["2023-01-15T14:30:00"]
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Date and time of the last update of the position",
        examples=["2023-02-20T10:15:00", None]
    )


class PositionPage(Page):
    """
    DTO for paginated response of positions.
    Represents a paginated collection of position data.
    """

    data: list[PositionResponseDTO] = Field(
        description="List of position objects in the current page",
        examples=[[{"id": 1, "nombre": "Project Manager", "created_at": "2023-01-15T14:30:00", "updated_at": None}]]
    )