from datetime import datetime
from src.app.schema import Page
from pydantic import BaseModel, Field


class HamletResponseDto(BaseModel):
    """
    DTO for Hamlet response.
    Contains all fields necessary to represent Hamlet information in API responses.
    """

    id: int = Field(
        ...,
        description="Unique identifier for the hamlet",
        gt=0,
        examples=[1],
    )
    nombre: str = Field(
        ...,
        description="Name of the hamlet",
        min_length=2,
        examples=["San Miguel", "El Paraíso"],
    )
    centro_poblado_id: int | None = Field(
        default=None,
        description="ID of the population center associated with the hamlet",
        gt=0,
        examples=[1],
    )
    centro_poblado_nombre: str | None = Field(
        default=None,
        description="Name of the population center associated with the hamlet",
        examples=["Centro Poblado San Miguel"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the hamlet was created",
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Timestamp of the last update to the hamlet",
    )


class HamletPage(Page):
    """
    DTO for paginated response of hamlets.
    Represents a paginated collection of hamlet data for listing purposes.
    """

    data: list[HamletResponseDto] = Field(
        ..., description="List of hamlet records in the current page"
    )
