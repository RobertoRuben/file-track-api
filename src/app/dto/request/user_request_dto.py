import re
from src.app.model.enum import StatusEnum
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class UserRequestDTO(BaseModel):
    """
    DTO for creating or updating a user.

    :ivar username: User's username. Must be at least 4 characters and contain at least one number
    :ivar password: User's password. Must have at least 8 characters, one uppercase letter, one number, and one special character
    :ivar is_active: User's status (Activate/Deactivate). If not provided, system default will be used
    :ivar role_id: ID of the role assigned to the user
    :ivar employee_id: ID of the employee associated with this user account
    """

    username: str = Field(
        ...,
        description="User's username. Must be at least 4 characters and contain at least one number.",
        min_length=4,
        examples=["john123", "admin2024"],
    )
    password: str = Field(
        ...,
        description="User's password. Must have at least 8 characters, one uppercase letter, one number, and one special character.",
        examples=["Secret@123", "P@ssw0rd!"],
    )
    is_active: StatusEnum | None = Field(
        default=None,
        description="User's status (Activate/Deactivate). If not provided, system default will be used.",
        examples=["Activate"],
    )
    role_id: int = Field(
        ..., description="ID of the role assigned to the user", examples=[1, 2]
    )
    employee_id: int = Field(
        ...,
        description="ID of the employee associated with this user account",
        examples=[1001, 2045],
    )

    @field_validator("username", mode="after")
    def validate_username_contains_number(cls, v):
        """
        Validates that the username contains at least one number.

        :param v: The username value to validate
        :return: The validated username
        :raises ValueError: If the username doesn't contain at least one number
        """
        if not re.search(r'[0-9]', v):
            raise ValueError("Username must contain at least one number")
        return v

    @field_validator("password", mode="after")
    def validate_password_strength(cls, v):
        """
        Validates that the password meets security requirements.

        :param v: The password value to validate
        :return: The validated password
        :raises ValueError: If the password doesn't meet security requirements
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r'[0-9]', v):
            raise ValueError("Password must contain at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError(
                "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
            )

        return v
