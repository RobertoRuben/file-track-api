from pydantic import BaseModel, Field
from datetime import datetime
from src.app.core.schema import Page


class DepartmentConnectionResponseDTO(BaseModel):
    """
    Data Transfer Object for department connection responses.
    Represents the data structure returned when querying department connections.

    :ivar id: Unique identifier for the department connection
    :ivar source_department_id: ID of the source department in the connection
    :ivar source_department_name: Name of the source department
    :ivar target_department_id: ID of the target department in the connection
    :ivar target_department_name: Name of the target department
    :ivar created_at: Timestamp when the connection was created
    :ivar updated_at: Timestamp when the connection was last updated
    """

    id: int = Field(
        ...,
        description="Unique identifier for the department connection",
        examples=[1],
    )
    source_department_id: int = Field(
        ..., description="ID of the source department", examples=[2]
    )
    source_department_name: str | None = Field(
        default=None,
        description="Name of the source department",
        examples=["Development"],
    )
    target_department_id: int = Field(
        ..., description="ID of the target department", examples=[3]
    )
    target_department_name: str | None = Field(
        default=None,
        description="Name of the target department",
        examples=["Human Resources"],
    )
    created_at: datetime | None = Field(
        default=None,
        description="Timestamp when the connection was created",
        examples=["2023-05-15T09:30:00"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Timestamp when the connection was last updated",
        examples=["2023-05-16T14:45:00"],
    )


class DepartmentConnectionPage(Page):
    """
    Data Transfer Object for paginated response of department connections.
    Represents a paginated collection of department connection data.

    :ivar data: List of department connection records in the current page
    :ivar meta: Pagination metadata information
    """

    data: list[DepartmentConnectionResponseDTO] = Field(
        ..., description="List of department connection records in the current page"
    )
