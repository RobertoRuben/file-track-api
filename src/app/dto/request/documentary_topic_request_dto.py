import re
from pydantic import BaseModel, Field, field_validator, ValidationInfo

class DocumentaryTopicRequestDTO(BaseModel):
    """
    DTO for creating or updating a documentary topic.
    """

    nombre: str = Field(description="Nombre del ambito documental", min_length=3)

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
            raise ValueError(f"{field_name} must be a string")

        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError(f"{field_name} cannot be empty or contain only spaces")

        return stripped_value

    @field_validator("nombre", mode="after")
    def validate_name_format(cls, v):
        """
        Validates that the name contains only alphabetic characters and spaces.

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
                "Department name must contain only alphabetic characters and single spaces between words"
            )
        return v
