from pydantic import BaseModel, Field
from datetime import datetime
from src.app.schema import Page


class AreaConnectionResponseDTO(BaseModel):
    """
    DTO for department communication response.
    Represents the data structure returned when querying department communications.
    """

    id: int = Field(
        ...,
        description="Unique identifier for the department communication",
        examples=[1],
    )
    area_origen_id: int = Field(
        ..., description="ID of the source department", examples=[2]
    )
    area_origen_nombre: str | None = Field(
        default=None,
        description="Name of the source department",
        examples=["Development"],
    )
    area_destino_id: int = Field(
        ..., description="ID of the destination department", examples=[3]
    )
    area_destino_nombre: str | None = Field(
        default=None,
        description="Name of the destination department",
        examples=["Human Resources"],
    )
    created_at: datetime | None = Field(
        default=None,
        description="Timestamp when the communication was created",
        examples=["2023-05-15T09:30:00"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Timestamp when the communication was last updated",
        examples=["2023-05-16T14:45:00"],
    )


class AreaConnectionPage(Page):
    """
    DTO for paginated response of department communications.
    Represents a paginated collection of department communication data.
    """

    data: list[AreaConnectionResponseDTO] = Field(
        ..., description="List of department communication records in the current page"
    )
