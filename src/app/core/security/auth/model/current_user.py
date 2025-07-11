from datetime import datetime
from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    """
    DTO for current user response.
    Represents the data structure returned when querying current user information.
    :ivar id: User's unique identifier
    :ivar username: User's login name used for authentication
    :ivar employee_name: Full name of the employee associated with this user
    :ivar role_name: Name of the role assigned to this user
    :ivar department_id: ID of the department associated with this user
    :ivar is_active: Indicates whether the user account is active or deactivated
    :ivar created_at: Timestamp when the user account was created
    :ivar updated_at: Timestamp when the user account was last updated
    """

    id: int = Field(..., description="User's unique identifier", examples=[1, 42])
    username: str = Field(
        ...,
        description="User's login name used for authentication",
        examples=["john123", "admin2024"],
    )
    employee_name: str = Field(
        ...,
        description="Full name of the employee associated with this user",
        examples=["John Smith", "Maria Rodriguez"],
    )
    role_name: str = Field(
        ...,
        description="Name of the role assigned to this user",
        examples=["Administrator", "Employee"],
    )
    department_id: int = Field(
        ...,
        description="ID of the department associated with this user",
        examples=[1, 2],
    )
    is_active: bool = Field(
        ...,
        description="Indicates whether the user account is active or deactivated",
        examples=[True, False],
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
