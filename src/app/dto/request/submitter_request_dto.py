import re
from src.app.model.enum import GeneroEnum
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class SubmitterRequestDTO(BaseModel):
    """
    DTO para crear o actualizar un remitente.
    """

    dni: int = Field(
        ..., description="Submitter's national ID number", ge=10000000, lt=100000000
    )
    nombres: str = Field(..., description="Submitter's first name", min_length=2)
    apellido_paterno: str = Field(
        ..., description="Submitter's paternal surname", min_length=2
    )
    apellido_materno: str = Field(
        ..., description="Submitter's maternal surname", min_length=2
    )
    genero: GeneroEnum = Field(..., description="Submitter's gender")

    @field_validator("nombres", "apellido_paterno", "apellido_materno", mode="before")
    def strip_and_validate_string(cls, v, info: ValidationInfo):
        """
        Valida que la entrada sea una cadena y elimina espacios en blanco.

        Args:
            v: El valor a validar
            info: Contexto de información de validación

        Returns:
            El valor de cadena sin espacios en blanco

        Raises:
            ValueError: Si el valor no es una cadena o está vacío después de eliminar espacios
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
        Valida que el DNI sea un número.

        Args:
            v: El valor a validar

        Returns:
            El valor numérico del DNI

        Raises:
            ValueError: Si el valor no es numérico o no cumple con el formato esperado
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
        Valida que el nombre/apellido contenga solo caracteres alfabéticos y espacios.

        Args:
            v: El valor de cadena a validar
            info: Contexto de información de validación

        Returns:
            El valor de cadena validado

        Raises:
            ValueError: Si el nombre/apellido contiene caracteres no válidos
        """
        field_name = info.field_name.replace("_", " ").title()
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$")

        if not pattern.fullmatch(v):
            raise ValueError(
                f"{field_name} debe contener solo caracteres alfabéticos y espacios simples entre palabras"
            )
        return v

    @field_validator("dni", mode="after")
    def validate_dni_length(cls, v):
        """
        Valida que el DNI tenga exactamente 8 dígitos.

        Args:
            v: El valor numérico del DNI

        Returns:
            El valor del DNI validado

        Raises:
            ValueError: Si el DNI no tiene exactamente 8 dígitos
        """
        if len(str(v)) != 8:
            raise ValueError("DNI must have exactly 8 digits")
        return v
