from datetime import datetime
from src.app.schema import Page
from pydantic import BaseModel, Field


class EmployeeResponseDTO(BaseModel):
    """
    DTO for employee response.
    Represents the data structure returned when querying employee information.
    """

    id: int = Field(..., description="Employee's unique identifier", examples=[1])
    dni: int = Field(
        ..., description="Employee's national ID number (8 digits)", examples=[12345678]
    )
    nombres: str = Field(
        ..., description="Employee's first name(s)", examples=["Juan Carlos"]
    )
    apellido_paterno: str = Field(
        ..., description="Employee's paternal surname", examples=["Pérez"]
    )
    apellido_materno: str = Field(
        ..., description="Employee's maternal surname", examples=["Gómez"]
    )
    genero: str = Field(
        ...,
        description="Employee's gender (Masculino/Femenino)",
        examples=["Masculino"],
    )
    cargo_id: int = Field(
        ..., description="ID of the employee's position", examples=[1]
    )
    cargo_nombre: str | None = Field(
        None,
        description="Name of the employee's position",
        examples=["Desarrollador Senior"],
    )
    area_id: int = Field(
        ..., description="ID of the employee's department", examples=[1]
    )
    area_nombre: str | None = Field(
        None, description="Name of the employee's department", examples=["Desarrollo"]
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
    """

    data: list[EmployeeResponseDTO] = Field(
        ..., description="List of employee records in the current page"
    )
