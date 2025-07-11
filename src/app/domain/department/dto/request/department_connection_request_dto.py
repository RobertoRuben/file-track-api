from pydantic import BaseModel, Field, field_validator, ValidationInfo


class DepartmentConnectionRequestDTO(BaseModel):
    """
    Data Transfer Object for department connection requests.
    Used to establish communication links between two departments in the organizational structure.

    :ivar source_department_id: ID of the source department in the connection
    :ivar target_department_id: ID of the target department in the connection
    """

    source_department_id: int = Field(
        ..., description="ID of the source department", gt=0, examples=[1]
    )

    target_department_id: int = Field(
        ..., description="ID of the target department", gt=0, examples=[2]
    )

    @field_validator("source_department_id", "target_department_id", mode="before")
    def validate_id_input(cls, v, info: ValidationInfo):
        """
        Validates that the department IDs are integers or can be converted to integer.

        :param v: The ID value to validate
        :param info: Validation information context
        :return: The ID value converted to integer
        :raises ValueError: If the ID cannot be converted to a positive integer
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

    @field_validator("source_department_id", "target_department_id", mode="after")
    def validate_positive_id(cls, v, info: ValidationInfo):
        """
        Validates that the department IDs are positive integers.

        :param v: The ID value to validate
        :param info: Validation information context
        :return: The validated ID value
        :raises ValueError: If the ID is not a positive integer
        """
        field_name = info.field_name.replace("_", " ").title()

        if v <= 0:
            raise ValueError(f"{field_name} must be a positive integer")

        return v

    @field_validator("target_department_id", mode="after")
    def validate_different_departments(cls, v, info: ValidationInfo):
        """
        Validates that source and target departments are different.

        :param v: The target department ID
        :param info: Validation information context
        :return: The validated target department ID
        :raises ValueError: If source and target IDs are the same
        """
        data = info.data

        if "source_department_id" in data and data["source_department_id"] == v:
            raise ValueError("Source and target departments cannot be the same")

        return v
