import re
from pydantic import BaseModel, Field, field_validator, ValidationInfo


class DocumentCategoryRequestDTO(BaseModel):
    """
    DTO for creating or updating a document category.

    :ivar name: The name of the document category
    """

    name: str = Field(
        ...,
        description="Name of the document category",
        min_length=3,
        examples=["Financial Documents", "Technical Reports", "Legal Contracts"],
    )

    @field_validator("name", mode="before")
    def strip_and_validate_string(cls, v, info: ValidationInfo):
        """
        Validates that the input is a string and strips whitespace.

        :param v: The value to validate
        :param info: Validation information context
        :return: The stripped string value
        :raises ValueError: If the value is not a string or is empty after stripping
        """
        field_name = info.field_name.replace("_", " ").title()

        if not isinstance(v, str):
            raise ValueError(f"{field_name} must be a string")

        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError(
                f"{field_name} cannot be empty or contain only whitespaces"
            )

        return stripped_value

    @field_validator("name", mode="after")
    def validate_name_format(cls, v):
        """
        Validates that the name contains only alphabetic characters and spaces.

        :param v: The string value to validate
        :return: The validated string value
        :raises ValueError: If the name contains invalid characters
        """
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$")
        if not pattern.fullmatch(v):
            raise ValueError(
                "Name must contain only alphabetic characters and simple spaces between words"
            )
        return v
