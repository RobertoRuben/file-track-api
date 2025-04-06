from pydantic import BaseModel, Field
from datetime import datetime
from src.app.schema import Page


class DocumentCategoryResponseDTO(BaseModel):
    """
    DTO for the response of a document category.
    Represents the data structure returned when querying document categories.

    :ivar id: The unique identifier for the document category
    :ivar name: The name of the document category
    :ivar created_at: The timestamp when the document category was created
    :ivar updated_at: The timestamp when the document category was last updated
    """

    id: int = Field(
        description="Unique ID of the document category", examples=[1, 2, 3]
    )
    name: str = Field(
        description="Name of the document category",
        examples=["Financial Documents", "Technical Reports", "Legal Contracts"],
    )
    created_at: datetime = Field(
        description="Creation date and time of the category",
        examples=["2023-01-15T14:30:00Z"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Last update date and time of the category",
        examples=["2023-02-20T09:45:00Z", None],
    )


class DocumentCategoryPage(Page):
    """
    DTO for paginated response of document categories.
    Represents a paginated collection of document category data.

    :ivar data: List of document categories in the current page
    :ivar meta: Pagination metadata
    """

    data: list[DocumentCategoryResponseDTO] = Field(
        description="List of document categories in the current page"
    )
