import re
from src.app.model.enum import StatusEnum
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class UserRequestDTO(BaseModel):
    """
    DTO for creating or updating a user.
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
    rol_id: int = Field(
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

        Args:
            v: The username value to validate

        Returns:
            The validated username

        Raises:
            ValueError: If the username doesn't contain at least one number
        """
        if not re.search(r'[0-9]', v):
            raise ValueError("Username must contain at least one number")
        return v

    @field_validator("password", mode="after")
    def validate_password_strength(cls, v):
        """
        Validates that the password meets security requirements.

        Args:
            v: The password value to validate

        Returns:
            The validated password

        Raises:
            ValueError: If the password doesn't meet security requirements
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
