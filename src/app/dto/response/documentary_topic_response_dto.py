from pydantic import BaseModel, Field
from datetime import datetime
from src.app.schema import Page

class DocumentaryTopicResponseDTO(BaseModel):
    """
    DTO for documentary topic responses.
    Represents the structure of the data returned in API responses.
    """

    id: int = Field(description="ID of the documentary topic")
    nombre: str = Field(description="Name of the documentary topic")
    created_at: datetime = Field(description="Creation date of the documentary topic")
    updated_at: datetime | None = Field(default=None, description="Last update date of the documentary topic")


class DocumentaryTopicPage(Page):
    """
    DTO for paginated response of documentary topics.
    Represents the structure of the data returned in API responses.
    """
    data: list[DocumentaryTopicResponseDTO] = Field(description="List of documentary topics")