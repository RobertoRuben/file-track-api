from pydantic import BaseModel, Field, field_validator, ValidationInfo


class AreaConnectionRequestDto(BaseModel):
    """
    DTO for department connection/communication requests.
    Used to establish communication links between two departments.
    """

    area_origen_id: int = Field(
        ..., description="ID of the source department", gt=0, examples=[1]
    )

    area_destino_id: int = Field(
        ..., description="ID of the destination department", gt=0, examples=[2]
    )

    @field_validator("area_origen_id", "area_destino_id", mode="before")
    def validate_id_input(cls, v, info: ValidationInfo):
        """
        Validates that the department IDs are integers or can be converted to integer.

        Args:
            v: The ID value to validate
            info: Validation information context

        Returns:
            The ID value converted to integer

        Raises:
            ValueError: If the ID cannot be converted to a positive integer
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

    @field_validator("area_origen_id", "area_destino_id", mode="after")
    def validate_positive_id(cls, v, info: ValidationInfo):
        """
        Validates that the department IDs are positive integers.

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

    @field_validator("area_destino_id", mode="after")
    def validate_different_departments(cls, v, info: ValidationInfo):
        """
        Validates that source and destination departments are different.

        Args:
            v: The destination department ID
            info: Validation information context

        Returns:
            The validated destination department ID

        Raises:
            ValueError: If source and destination IDs are the same
        """
        data = info.data

        if "area_origen_id" in data and data["area_origen_id"] == v:
            raise ValueError("Source and destination departments cannot be the same")

        return v
