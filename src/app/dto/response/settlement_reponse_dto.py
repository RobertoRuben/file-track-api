from src.app.schema import Page
from pydantic import BaseModel, Field
from datetime import datetime


class SettlementResponseDTO(BaseModel):
    """
    DTO for settlement response.
    Represents the data structure returned when querying settlements.

    :ivar id: The unique identifier for the settlement
    :ivar name: The name of the settlement
    :ivar created_at: The timestamp when the settlement was created
    :ivar updated_at: The timestamp when the settlement was last updated
    """

    id: int = Field(description="Unique settlement ID", examples=[1, 2, 3])
    name: str = Field(
        description="Name of the settlement",
        examples=["San Isidro", "Santa Fe", "Villa Maria"],
    )
    created_at: datetime = Field(
        description="Settlement creation date and time",
        examples=["2023-10-15T14:30:00Z"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Last update date and time of the settlement",
        examples=["2023-11-20T09:45:00Z", None],
    )


class SettlementPage(Page):
    """
    DTO for paginated response of settlements.
    Represents a paginated collection of settlement data.

    :ivar data: List of settlements in the current page
    :ivar meta: Pagination metadata
    """

    data: list[SettlementResponseDTO] = Field(
        description="List of settlements in the current page",
        examples=[
            [
                {
                    "id": 1,
                    "name": "San Isidro",
                    "created_at": "2023-10-15T14:30:00Z",
                    "updated_at": "2023-11-20T09:45:00Z",
                },
                {
                    "id": 2,
                    "name": "Santa Fe",
                    "created_at": "2023-10-16T10:20:00Z",
                    "updated_at": None,
                },
            ]
        ],
    )
