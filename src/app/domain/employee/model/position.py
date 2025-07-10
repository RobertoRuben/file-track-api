from sqlmodel import (
    BIGINT,
    TEXT,
    CheckConstraint,
    Column,
    DateTime,
    Field,
    SQLModel,
    text,
    Relationship,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .employee import Employee


class Position(SQLModel, table=True):
    """
    Represents a job position within the organization.

    :ivar id: The unique identifier for the position
    :ivar name: The name of the position
    :ivar created_at: The timestamp when the position was created
    :ivar updated_at: The timestamp when the position was last updated
    :ivar employees: List of employees who hold this position
    """

    __tablename__ = "positions"
    __table_args__ = (CheckConstraint("LENGTH(name) > 3", name="ck_position_name"),)

    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    name: str = Field(default=None, sa_column=Column(TEXT, unique=True))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    employees: list["Employee"] = Relationship(back_populates="position")
