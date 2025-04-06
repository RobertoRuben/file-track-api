from sqlmodel import (
    BIGINT,
    UniqueConstraint,
    Column,
    DateTime,
    Field,
    SQLModel,
    ForeignKey,
    text,
    Relationship,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .department import Department


class DepartmentConnection(SQLModel, table=True):
    """
    Represents a connection between two departments in the organizational structure.

    :ivar id: The unique identifier for the department connection
    :ivar source_department_id: The ID of the source department
    :ivar target_department_id: The ID of the target department
    :ivar created_at: The timestamp when the connection was created
    :ivar updated_at: The timestamp when the connection was last updated
    :ivar source_department: The source department in the connection
    :ivar target_department: The target department in the connection
    """

    __tablename__ = "department_connections"
    __table_args__ = (
        UniqueConstraint(
            "source_department_id",
            "target_department_id",
            name="uq_department_connections_source_target",
        ),
    )
    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    source_department_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "departments.id",
                name="fk_department_connections_source",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    target_department_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "departments.id",
                name="fk_department_connections_target",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    source_department: "Department" = Relationship(
        back_populates="outgoing_connections",
        sa_relationship_kwargs={
            "primaryjoin": "Department.id == DepartmentConnection.source_department_id",
        },
    )
    target_department: "Department" = Relationship(
        back_populates="incoming_connections",
        sa_relationship_kwargs={
            "primaryjoin": "Department.id == DepartmentConnection.target_department_id",
        },
    )
