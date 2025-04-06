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

    id: int = Field(
        description="Unique ID of the department in the institution", examples=[1, 2, 3]
    )
    name: str = Field(
        description="Name of the department in the institution",
        examples=["Recursos Humanos", "Finanzas", "Tecnología"],
    )
    created_at: datetime = Field(
        description="Date and time when the department was created",
        examples=["2023-10-15T14:30:00.000Z"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Date and time of the last department update",
        examples=["2023-11-20T09:45:32.000Z", None],
    )


class DepartmentPage(Page):
    """
    DTO for paginated response of departments.
    Represents a paginated collection of department data.

    :ivar data: List of department response DTOs
    """

    data: list[DepartmentResponseDTO] = Field(
        description="List of departments with their details",
        examples=[
            [
                {
                    "id": 1,
                    "name": "Recursos Humanos",
                    "created_at": "2023-10-15T14:30:00.000Z",
                    "updated_at": "2023-11-20T09:45:32.000Z",
                },
                {
                    "id": 2,
                    "name": "Finanzas",
                    "created_at": "2023-09-05T10:15:00.000Z",
                    "updated_at": None,
                },
            ]
        ],
    )
