from datetime import datetime
from src.app.schema import Page
from pydantic import BaseModel, Field


class EmployeeResponseDTO(BaseModel):
    """
    DTO for employee response.
    Represents the data structure returned when querying employee information.

    :ivar id: The employee's unique identifier
    :ivar dni: The employee's national ID number (8 digits)
    :ivar names: The employee's first name(s)
    :ivar paternal_surname: The employee's paternal surname
    :ivar maternal_surname: The employee's maternal surname
    :ivar gender: The employee's gender (Male/Female)
    :ivar position_id: The ID of the employee's position
    :ivar position_name: The name of the employee's position
    :ivar department_id: The ID of the employee's department
    :ivar department_name: The name of the employee's department
    :ivar created_at: Timestamp when the employee record was created
    :ivar updated_at: Timestamp when the employee record was last updated
    """

    id: int = Field(..., description="Employee's unique identifier", examples=[1])
    dni: int = Field(
        ..., description="Employee's national ID number (8 digits)", examples=[12345678]
    )
    names: str = Field(
        ..., description="Employee's first name(s)", examples=["Juan Carlos"]
    )
    paternal_surname: str = Field(
        ..., description="Employee's paternal surname", examples=["Pérez"]
    )
    maternal_surname: str = Field(
        ..., description="Employee's maternal surname", examples=["Gómez"]
    )
    gender: str = Field(
        ...,
        description="Employee's gender (Male/Female)",
        examples=["Male"],
    )
    position_id: int = Field(
        ..., description="ID of the employee's position", examples=[1]
    )
    position_name: str | None = Field(
        None,
        description="Name of the employee's position",
        examples=["Senior Developer"],
    )
    department_id: int = Field(
        ..., description="ID of the employee's department", examples=[1]
    )
    department_name: str | None = Field(
        None, description="Name of the employee's department", examples=["Development"]
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the employee record was created",
        examples=["2025-03-25T10:30:00"],
    )
    updated_at: datetime | None = Field(
        None,
        description="Timestamp when the employee record was last updated",
        examples=["2025-03-26T15:45:00"],
    )


class EmployeePage(Page):
    """
    DTO for paginated response of employees.
    Represents a paginated collection of employee data for listing purposes.

    :ivar data: List of employee records in the current page
    """

    data: list[EmployeeResponseDTO] = Field(
        ..., description="List of employee records in the current page"
    )
