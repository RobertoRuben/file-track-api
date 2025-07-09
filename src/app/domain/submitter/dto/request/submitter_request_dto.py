import re
from src.app.model.enum import GeneroEnum
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class SubmitterRequestDTO(BaseModel):
    """
    DTO for creating or updating a submitter.

    :ivar dni: National identification number (8 digits)
    :ivar names: First and middle names of the submitter
    :ivar paternal_surname: Paternal last name
    :ivar maternal_surname: Maternal last name
    :ivar gender: Gender of the submitter (Male/Female)
    """

    dni: int = Field(
        ...,
        description="Submitter's national ID number",
        ge=10000000,
        lt=100000000,
        examples=[48756321],
    )
    names: str = Field(
        ...,
        description="Submitter's first name",
        min_length=2,
        examples=["Juan Carlos"],
    )
    paternal_surname: str = Field(
        ...,
        description="Submitter's paternal surname",
        min_length=2,
        examples=["García"],
    )
    maternal_surname: str = Field(
        ...,
        description="Submitter's maternal surname",
        min_length=2,
        examples=["Rodríguez"],
    )
    gender: GeneroEnum = Field(..., description="Submitter's gender", examples=["Male"])

    @field_validator("names", "paternal_surname", "maternal_surname", mode="before")
    def strip_and_validate_string(cls, v, info: ValidationInfo):
        """
        Validates that the input is a string and strips whitespace.

        :param v: Value to validate
        :param info: Validation context information
        :return: Stripped string value
        :raises ValueError: If value is not a string or is empty after stripping
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
        Validates that DNI is a numeric value.

        :param v: Value to validate
        :return: Numeric value of DNI
        :raises ValueError: If value is not numeric or doesn't meet expected format
        """
        if isinstance(v, str):
            v = v.strip()
            if not v.isdigit():
                raise ValueError("DNI must contain only numeric digits")
            v = int(v)

        if not isinstance(v, int):
            raise ValueError("DNI must be an integer")

        return v

    @field_validator("names", "paternal_surname", "maternal_surname", mode="after")
    def validate_name_format(cls, v, info: ValidationInfo):
        """
        Validates that name/surname contains only alphabetic characters and spaces.

        :param v: String value to validate
        :param info: Validation context information
        :return: Validated string value
        :raises ValueError: If name/surname contains invalid characters
        """
        field_name = info.field_name.replace("_", " ").title()
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$")

        if not pattern.fullmatch(v):
            raise ValueError(
                f"{field_name} must contain only alphabetic characters and spaces between words"
            )
        return v

    @field_validator("dni", mode="after")
    def validate_dni_length(cls, v):
        """
        Validates that DNI has exactly 8 digits.

        :param v: Numeric DNI value
        :return: Validated DNI value
        :raises ValueError: If DNI doesn't have exactly 8 digits
        """
        if len(str(v)) != 8:
            raise ValueError("DNI must have exactly 8 digits")
        return v
