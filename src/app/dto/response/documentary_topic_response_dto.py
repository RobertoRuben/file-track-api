from pydantic import BaseModel, Field
from datetime import datetime
from src.app.schema import Page


class DocumentaryTopicResponseDTO(BaseModel):
    """
    DTO for documentary topic responses.
    Represents the structure of the data returned in API responses.

    :ivar id: The unique identifier of the documentary topic
    :ivar name: The name of the documentary topic
    :ivar created_at: The timestamp when the documentary topic was created
    :ivar updated_at: The timestamp when the documentary topic was last updated, or None if never updated
    """

    id: int = Field(description="ID of the documentary topic", examples=[1, 2, 3])
    name: str = Field(
        description="Name of the documentary topic",
        examples=["Legal Documentation", "Technical Reports", "Academic Research"],
    )
    created_at: datetime = Field(
        description="Creation date of the documentary topic",
        examples=["2023-05-15T10:30:00"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Last update date of the documentary topic",
        examples=[None, "2023-06-01T14:20:00"],
    )


class DocumentaryTopicPage(Page):
    """
    DTO for paginated response of documentary topics.
    Represents the structure of the data returned in API responses.

    :ivar data: List of documentary topics in the current page
    :ivar meta: Pagination metadata including page information
    """

    data: list[DocumentaryTopicResponseDTO] = Field(
        description="List of documentary topics"
    )
