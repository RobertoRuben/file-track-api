import re
from pydantic import BaseModel, Field, field_validator, ValidationInfo

class CategoryDocumentRequestDTO(BaseModel):
    """
    DTO for creating or updating a document category.
    """
    nombre: str = Field(..., description="Nombre de la categoría del documento", min_length=3)

    @field_validator("nombre", mode="before")
    def strip_and_validate_string(cls, v, info: ValidationInfo):
        field_name = info.field_name.replace("_", " ").title()

        if not isinstance(v, str):
            raise ValueError(f"{field_name} debe ser una cadena de texto")

        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError(f"{field_name} no puede estar vacío o contener solo espacios")

        return stripped_value

    @field_validator("nombre", mode="after")
    def validate_name_format(cls, v):
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$")
        if not pattern.fullmatch(v):
            raise ValueError(
                "El nombre debe contener solo caracteres alfabéticos y espacios simples entre palabras"
            )
        return v