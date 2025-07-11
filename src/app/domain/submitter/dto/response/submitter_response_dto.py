from datetime import datetime
from pydantic import BaseModel, Field
from src.app.core.schema import Page


class SubmitterResponseDTO(BaseModel):
    """
    DTO for submitter response.
    Represents the data structure returned when querying submitters.

    :ivar id: Unique identifier of the submitter
    :ivar dni: National identification number
    :ivar names: First and middle names of the submitter
    :ivar paternal_surname: Paternal last name
    :ivar maternal_surname: Maternal last name
    :ivar gender: Gender of the submitter
    :ivar created_at: Timestamp when the submitter was created
    :ivar updated_at: Timestamp when the submitter was last updated, if any
    """

    id: int = Field(..., description="Submitter's ID", examples=[1])
    dni: int = Field(
        ..., description="Submitter's national ID number", examples=[48756321]
    )
    names: str = Field(
        ..., description="Submitter's first name", examples=["Juan Carlos"]
    )
    paternal_surname: str = Field(
        ..., description="Submitter's paternal surname", examples=["García"]
    )
    maternal_surname: str = Field(
        ..., description="Submitter's maternal surname", examples=["Rodríguez"]
    )
    gender: str = Field(..., description="Submitter's gender", examples=["Male"])
    created_at: datetime = Field(
        ...,
        description="Timestamp when the submitter was created",
        examples=["2023-05-17T10:30:45.123456"],
    )
    updated_at: datetime | None = Field(
        None,
        description="Timestamp when the submitter was last updated",
        examples=["2023-06-20T15:45:22.987654"],
    )


class SubmitterPage(Page):
    """
    DTO for paginated response of submitters.
    Represents a paginated collection of submitter data.

    :ivar data: List of submitter objects
    :ivar meta: Pagination metadata
    """

    data: list[SubmitterResponseDTO] = Field(..., description="List of submitters")
