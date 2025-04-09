import re
from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator
from src.app.model.enum import GeneroEnum


class EmployeeRequestDTO(BaseModel):
    """
    DTO for employee creation and update requests.
    Contains all fields necessary to process employee information.

    :ivar dni: The national identification number of the employee (8 digits)
    :ivar names: The employee's first names
    :ivar paternal_surname: The paternal surname of the employee
    :ivar maternal_surname: The maternal surname of the employee
    :ivar gender: The gender of the employee
    :ivar position_id: The ID of the position associated with the employee
    :ivar department_id: The ID of the department associated with the employee
    """

    dni: int = Field(
        ...,
        description="Employee's national identification number",
        ge=10000000,
        lt=100000000,
        examples=[12345678],
    )
    names: str = Field(
        ...,
        description="Employee's first names",
        min_length=2,
        examples=["Juan Carlos"],
    )
    paternal_surname: str = Field(
        ...,
        description="Employee's paternal surname",
        min_length=2,
        examples=["Pérez"],
    )
    maternal_surname: str = Field(
        ...,
        description="Employee's maternal surname",
        min_length=2,
        examples=["Gómez"],
    )
    gender: GeneroEnum = Field(
        ..., description="Employee's gender", examples=["Male", "Female"]
    )
    position_id: int = Field(
        ...,
        description="ID of the position associated with the employee",
        gt=0,
        examples=[1],
    )
    department_id: int = Field(
        ...,
        description="ID of the department associated with the employee",
        gt=0,
        examples=[1],
    )

    @field_validator("names", "paternal_surname", "maternal_surname", mode="before")
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
            raise ValueError(f"{field_name} must be a text string")

        stripped_value = v.strip()
        if not stripped_value:
            raise ValueError(f"{field_name} cannot be empty or contain only spaces")

        return stripped_value

    @field_validator("dni", mode="before")
    def validate_dni_is_numeric(cls, v):
        """
        Validates that the DNI is a number.

        :param v: The value to validate
        :return: The numeric value of the DNI
        :raises ValueError: If the value is not numeric or doesn't meet the expected format
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
        Validates that the name/surname contains only alphabetic characters and spaces.

        :param v: The string value to validate
        :param info: Validation information context
        :return: The validated string value
        :raises ValueError: If the name/surname contains invalid characters
        """
        field_name = info.field_name.replace("_", " ").title()
        pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ][A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$")

        if not pattern.fullmatch(v):
            raise ValueError(
                f"{field_name} must contain only alphabetic characters and single spaces between words"
            )
        return v

    @field_validator("dni", mode="after")
    def validate_dni_length(cls, v):
        """
        Validates that the DNI has exactly 8 digits.

        :param v: The numeric value of the DNI
        :return: The validated DNI value
        :raises ValueError: If the DNI doesn't have exactly 8 digits
        """
        if len(str(v)) != 8:
            raise ValueError("DNI must have exactly 8 digits")
        return v

    @field_validator("position_id", "department_id", mode="before")
    def validate_ids_input(cls, v, info: ValidationInfo):
        """
        Validates that the input IDs are integers or can be converted to integers.

        :param v: The ID value to validate
        :param info: Validation information context
        :return: The ID value converted to integer
        :raises ValueError: If the ID cannot be converted to an integer
        """
        field_name = info.field_name.replace("_", " ").title()

        if isinstance(v, str):
            v = v.strip()
            if not v.isdigit():
                raise ValueError(f"{field_name} must contain only numeric digits")
            v = int(v)

        if not isinstance(v, int):
            raise ValueError(f"{field_name} must be an integer")

        return v

    @field_validator("position_id", "department_id", mode="after")
    def validate_ids(cls, v, info: ValidationInfo):
        """
        Validates that IDs are positive integers.

        :param v: The ID value to validate
        :param info: Validation information context
        :return: The validated ID value
        :raises ValueError: If the ID is not a positive integer
        """
        field_name = info.field_name.replace("_", " ").title()

        if v <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return v

    @model_validator(mode='before')
    def validate_numeric_fields(cls, data, info: ValidationInfo):
        """
        Validates numeric fields before Pydantic performs type validation.

        :param data: Raw input data from the request
        :param info: Validation information context
        :return: The validated data
        :raises ValueError: If numeric fields contain non-digit characters
        """
        if not isinstance(data, dict):
            return data

        numeric_fields = ["dni", "position_id", "department_id"]
        error_fields = []

        for field in numeric_fields:
            if field in data and isinstance(data[field], str):
                value = data[field].strip()
                if not value.isdigit():
                    field_name = field.replace("_", " ").title()
                    error_fields.append(
                        f"{field_name} must contain only numeric digits"
                    )

        if error_fields:
            raise ValueError(", ".join(error_fields))

        return data
