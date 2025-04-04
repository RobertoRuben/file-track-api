from sqlmodel import (
    SQLModel,
    text,
    Field,
    Column,
    CheckConstraint,
    BIGINT,
    TEXT,
    DateTime,
    Relationship,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Role(SQLModel, table=True):
    """
    Represents a user role within the system.

    :ivar id: The unique identifier for the role
    :ivar name: The name of the role
    :ivar created_at: The timestamp when the role was created
    :ivar updated_at: The timestamp when the role was last updated
    :ivar users: List of users assigned to this role
    """

    __tablename__ = "roles"
    __table_args__ = (CheckConstraint("LENGTH(name) > 3", name="ck_role_name"),)

    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    name: str = Field(sa_column=Column(TEXT, nullable=False, unique=True))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    users: list["User"] = Relationship(back_populates="role")
