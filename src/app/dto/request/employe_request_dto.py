import re
from pydantic import BaseModel, Field, ValidationInfo, field_validator
from src.app.model.enum import GeneroEnum


class EmployeeRequestDto(BaseModel):
    dni: int = Field(
        ...,
        description="Employee's national ID number",
        ge=10000000,
        lt=100000000,
        examples=[12345678],
    )
    nombres: str = Field(
        ..., description="Employee's first name", min_length=2, examples=["Juan Carlos"]
    )
    apellido_paterno: str = Field(
        ..., description="Employee's paternal surname", min_length=2, examples=["Pérez"]
    )
    apellido_materno: str = Field(
        ..., description="Employee's maternal surname", min_length=2, examples=["Gómez"]
    )
    genero: GeneroEnum = Field(
        ..., description="Employee's gender", examples=["Masculino", "Femenino"]
    )
    cargo_id: int = Field(
        ..., description="Position ID associated with the employee", gt=0, examples=[1]
    )
    area_id: int = Field(
        ...,
        description="Department ID associated with the employee",
        gt=0,
        examples=[1],
    )

    @field_validator("nombres", "apellido_paterno", "apellido_materno", mode="before")
    def strip_and_validate_string(cls, v, info: ValidationInfo):
        """
        Validates that the input is a string and removes whitespace.

        Args:
            v: The value to validate
            info: Validation information context

        Returns:
            The string value without whitespace

        Raises:
            ValueError: If the value is not a string or is empty after stripping
        """
        field_name = info.field_name.replace("_", " ").title()

        if not isinstance(v, str):
            raise ValueError(f"{field_name} must be a text string")

        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError(f"{field_name} cannot be empty or contain only spaces")

        return stripped_value

    @field_validator("dni", mode="before")
    def validate_dni_is_numeric(cls, v):
        """
        Validates that the DNI is a number.

        Args:
            v: The value to validate

        Returns:
            The numerical value of the DNI

        Raises:
            ValueError: If the value is not numeric or does not meet the expected format
        """
        if isinstance(v, str):
            v = v.strip()
            if not v.isdigit():
                raise ValueError("DNI must contain only numeric digits")
            v = int(v)

        if not isinstance(v, int):
            raise ValueError("DNI must be an integer")

        return v

    @field_validator("nombres", "apellido_paterno", "apellido_materno", mode="after")
    def validate_name_format(cls, v, info: ValidationInfo):
        """
        Validates that the name/surname contains only alphabetic characters and spaces.

        Args:
            v: The string value to validate
            info: Validation information context

        Returns:
            The validated string value

        Raises:
            ValueError: If the name/surname contains invalid characters
        """
        field_name = info.field_name.replace("_", " ").title()
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$")

        if not pattern.fullmatch(v):
            raise ValueError(
                f"{field_name} must contain only alphabetic characters and simple spaces between words"
            )
        return v

    @field_validator("dni", mode="after")
    def validate_dni_length(cls, v):
        """
        Validates that the DNI has exactly 8 digits.

        Args:
            v: The numeric value of the DNI

        Returns:
            The validated DNI value

        Raises:
            ValueError: If the DNI does not have exactly 8 digits
        """
        if len(str(v)) != 8:
            raise ValueError("DNI must have exactly 8 digits")
        return v

    @field_validator("cargo_id", "area_id", mode="after")
    def validate_ids(cls, v, info: ValidationInfo):
        """
        Validates that the IDs are positive integers.

        Args:
            v: The ID value to validate
            info: Validation information context

        Returns:
            The validated ID value

        Raises:
            ValueError: If the ID is not a positive integer
        """
        field_name = info.field_name.replace("_", " ").title()

        if v <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return v
