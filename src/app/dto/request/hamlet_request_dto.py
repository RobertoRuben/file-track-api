import re
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class HamletRequestDTO(BaseModel):
    """
    DTO for Hamlet request.
    Contains all fields necessary to process hamlet information for creation and update.
    """

    nombre: str = Field(
        ...,
        description="Name of the hamlet",
        min_length=2,
        examples=["San Miguel", "El Paraíso"],
    )
    centro_poblado_id: int | None = Field(
        None,
        description="ID of the population center associated with the hamlet",
        gt=0,
        examples=[1],
    )

    @field_validator("nombre", mode="before")
    def strip_and_validate_string(cls, v, info: ValidationInfo):
        """
        Validates that the input is a string and strips whitespace.

        Args:
            v: The value to validate
            info: Validation information context

        Returns:
            The stripped string value

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

    @field_validator("nombre", mode="after")
    def validate_name_format(cls, v):
        """
        Validates that the hamlet name contains only alphabetic characters and spaces.

        Args:
            v: The string value to validate

        Returns:
            The validated string value

        Raises:
            ValueError: If the name contains invalid characters
        """
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$")
        if not pattern.fullmatch(v):
            raise ValueError(
                "Hamlet name must contain only alphabetic characters and single spaces between words"
            )
        return v

    @field_validator("centro_poblado_id", mode="before")
    def validate_id_input(cls, v, info: ValidationInfo):
        """
        Validates that the center ID is an integer or can be converted to integer.
        Skips validation if the value is None.

        Args:
            v: The ID value to validate
            info: Validation information context

        Returns:
            The ID value converted to integer or None

        Raises:
            ValueError: If the ID cannot be converted to an integer
        """
        if v is None:
            return None

        field_name = info.field_name.replace("_", " ").title()

        if isinstance(v, str):
            v = v.strip()
            if not v.isdigit():
                raise ValueError(f"{field_name} must contain only numeric digits")
            v = int(v)

        if not isinstance(v, int):
            raise ValueError(f"{field_name} must be an integer")

        return v

    @field_validator("centro_poblado_id", mode="after")
    def validate_id(cls, v, info: ValidationInfo):
        """
        Validates that the center ID is a positive integer.
        Skips validation if the value is None.

        Args:
            v: The ID value to validate
            info: Validation information context

        Returns:
            The validated ID value or None

        Raises:
            ValueError: If the ID is not a positive integer
        """
        if v is None:
            return None

        field_name = info.field_name.replace("_", " ").title()

        if v <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return v
