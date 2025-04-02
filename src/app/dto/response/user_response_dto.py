from pydantic import BaseModel, Field
from datetime import datetime
from src.app.schema import Page


class UserResponseDTO(BaseModel):
    """
    DTO for user response.
    Represents the data structure returned when querying user information.
    """

    id: int = Field(..., description="User's unique identifier", examples=[1, 42])
    username: str = Field(
        ...,
        description="User's login name used for authentication",
        examples=["john123", "admin2024"],
    )
    is_active: bool = Field(
        ...,
        description="Indicates whether the user account is active or deactivated",
        examples=[True, False],
    )
    rol_id: int = Field(
        ..., description="ID of the role assigned to the user", examples=[1, 2]
    )
    role_name: str | None = Field(
        default=None,
        description="Name of the role assigned to this user",
        examples=["Administrator", "Employee"],
    )
    employee_id: int = Field(
        ...,
        description="ID of the employee associated with this user account",
        examples=[1001, 2045],
    )
    employee_name: str | None = Field(
        default=None,
        description="Full name of the employee associated with this user",
        examples=["John Smith", "Maria Rodriguez"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the user account was created",
        examples=["2023-06-15T10:30:00"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Timestamp when the user account was last updated",
        examples=["2023-07-20T15:45:00"],
    )


class UserPage(Page):
    """
    DTO for paginated response of users.
    Represents a paginated collection of user data for listing purposes.
    """

    data: list[UserResponseDTO] = Field(
        ..., description="List of user records in the current page"
    )
