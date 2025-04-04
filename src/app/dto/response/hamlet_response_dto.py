from datetime import datetime
from src.app.schema import Page
from pydantic import BaseModel, Field


class HamletResponseDTO(BaseModel):
    """
    DTO for Hamlet response.
    Contains all fields necessary to represent Hamlet information in API responses.

    :ivar id: Unique identifier for the hamlet
    :ivar name: Name of the hamlet
    :ivar settlement_id: ID of the settlement associated with the hamlet
    :ivar settlement_name: Name of the settlement associated with the hamlet
    :ivar created_at: Timestamp when the hamlet was created
    :ivar updated_at: Timestamp of the last update to the hamlet
    """

    id: int = Field(
        ...,
        description="Unique identifier for the hamlet",
        gt=0,
        examples=[1],
    )
    name: str = Field(
        ...,
        description="Name of the hamlet",
        min_length=2,
        examples=["San Miguel", "El Paraíso"],
    )
    settlement_id: int | None = Field(
        default=None,
        description="ID of the settlement associated with the hamlet",
        gt=0,
        examples=[1],
    )
    settlement_name: str | None = Field(
        default=None,
        description="Name of the settlement associated with the hamlet",
        examples=["San Miguel Settlement"],
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

    :ivar data: List of hamlet records in the current page
    """

    data: list[HamletResponseDTO] = Field(
        ..., description="List of hamlet records in the current page"
    )
