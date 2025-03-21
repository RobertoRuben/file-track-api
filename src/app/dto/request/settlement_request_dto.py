import re
from pydantic import BaseModel, field_validator, ValidationInfo

class SettlementRequestDTO(BaseModel):
    """
    DTO for creating or updating a settlement.
    """
    nombre: str

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
            raise ValueError(f"{field_name} debe ser una cadena de texto")

        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError(f"{field_name} no puede estar vacío o contener solo espacios")

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
                "El nombre debe contener solo caracteres alfabéticos y espacios simples entre palabras"
            )
        return v