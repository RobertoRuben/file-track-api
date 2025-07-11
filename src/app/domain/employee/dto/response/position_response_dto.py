from datetime import datetime
from pydantic import BaseModel, Field
from src.app.core.schema import Page


class PositionResponseDTO(BaseModel):
    """
    DTO for position response.
    Represents the data structure returned when querying positions.

    :ivar id: The unique identifier for the position
    :ivar name: The name of the position
    :ivar created_at: The timestamp when the position was created
    :ivar updated_at: The timestamp when the position was last updated
    """

    id: int = Field(description="Unique position ID", examples=[1, 2, 3])
    name: str = Field(
        description="Position name",
        examples=["Project Manager", "Developer", "Designer"],
    )
    created_at: datetime = Field(
        description="Creation date and time of the position",
        examples=["2023-01-15T14:30:00"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Date and time of the last update of the position",
        examples=["2023-02-20T10:15:00", None],
    )


class PositionPage(Page):
    """
    DTO for paginated response of positions.
    Represents a paginated collection of position data.

    :ivar data: List of position objects in the current page
    :ivar meta: Pagination metadata
    """

    data: list[PositionResponseDTO] = Field(
        description="List of position objects in the current page",
        examples=[
            [
                {
                    "id": 1,
                    "name": "Project Manager",
                    "created_at": "2023-01-15T14:30:00",
                    "updated_at": None,
                },
                {
                    "id": 2,
                    "name": "Developer",
                    "created_at": "2023-01-16T09:45:00",
                    "updated_at": "2023-03-10T14:20:00",
                },
            ]
        ],
    )
