from pydantic import BaseModel, Field
from datetime import datetime
from src.app.schema import Page


class RoleResponseDTO(BaseModel):
    """
    DTO for role responses.
    Represents the data structure returned when querying roles.

    :ivar id: The unique identifier of the role
    :ivar name: The name of the role
    :ivar created_at: The creation date and time of the role
    :ivar updated_at: The last update date and time of the role
    """

    id: int = Field(description="Unique role ID", examples=[1, 2, 3])
    name: str = Field(
        description="Role name", examples=["Administrator", "Editor", "Supervisor"]
    )
    created_at: datetime = Field(
        description="Role creation date and time",
        examples=["2023-10-15T14:30:00Z"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Last update date and time of the role",
        examples=["2023-11-20T09:45:00Z", None],
    )


class RolePage(Page):
    """
    DTO for paginated role responses.
    Represents a paginated collection of role data.

    :ivar data: List of roles in the current page
    """

    data: list[RoleResponseDTO]
