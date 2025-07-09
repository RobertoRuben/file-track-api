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
    from src.app.domain.employee.model import Employee
    from .department_connection import DepartmentConnection


class Department(SQLModel, table=True):
    """
    Represents a department or area within the organization.

    :ivar id: The unique identifier for the department
    :ivar name: The name of the department
    :ivar created_at: The timestamp when the department was created
    :ivar updated_at: The timestamp when the department was last updated
    :ivar employees: List of employees who belong to this department
    :ivar outgoing_connections: List of connections where this department is the source
    :ivar incoming_connections: List of connections where this department is the destination
    """

    __tablename__ = "departments"
    __table_args__ = (CheckConstraint("LENGTH(name) > 3", name="ck_department_name"),)

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

    employees: list["Employee"] = Relationship(back_populates="department")

    outgoing_connections: list["DepartmentConnection"] = Relationship(
        back_populates="source_department",
        sa_relationship_kwargs={
            "primaryjoin": "Department.id == DepartmentConnection.source_department_id",
        },
    )
    incoming_connections: list["DepartmentConnection"] = Relationship(
        back_populates="target_department",
        sa_relationship_kwargs={
            "primaryjoin": "Department.id == DepartmentConnection.target_department_id",
        },
    )
