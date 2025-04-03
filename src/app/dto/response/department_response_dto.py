from datetime import datetime
from pydantic import BaseModel, Field
from src.app.schema import Page


class DepartmentResponseDTO(BaseModel):
    """
    DTO for the response of a department.
    Represents the data structure returned when querying departments.

    :ivar id: Unique ID of the department in the institution
    :ivar name: Name of the department in the institution
    :ivar created_at: Date and time when the department was created
    :ivar updated_at: Date and time of the last department update
    """

    id: int = Field(description="Unique ID of the department in the institution")
    name: str = Field(description="Name of the department in the institution")
    created_at: datetime = Field(
        description="Date and time when the department was created"
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Date and time of the last department update",
    )


class DepartmentPage(Page):
    """
    DTO for paginated response of departments.
    Represents a paginated collection of department data.

    :ivar data: List of department response DTOs
    """

    data: list[DepartmentResponseDTO]
