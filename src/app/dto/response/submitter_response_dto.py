from datetime import datetime
from src.app.schema import Page
from pydantic import BaseModel, Field


class SubmitterResponseDTO(BaseModel):
    """
    DTO for settlement response.
    Represents the data structure returned when querying settlements.
    """

    id: int = Field(..., description="Submitter's ID")
    dni: int = Field(..., description="Submitter's national ID number")
    nombres: str = Field(..., description="Submitter's first name")
    apellido_paterno: str = Field(..., description="Submitter's paternal surname")
    apellido_materno: str = Field(..., description="Submitter's maternal surname")
    genero: str = Field(..., description="Submitter's gender")
    created_at: datetime = Field(
        ..., description="Timestamp when the submitter was created"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp when the submitter was last updated"
    )


class SubmitterPage(Page):
    """
    DTO for paginated response of settlements.
    Represents a paginated collection of settlement data.
    """

    data: list[SubmitterResponseDTO] = Field(..., description="List of settlements")
