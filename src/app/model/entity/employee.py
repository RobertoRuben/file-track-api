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
    ForeignKey,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app.domain.department.model.department import Department
    from .position import Position
    from .user import User


class Employee(SQLModel, table=True):
    """
    Represents an employee in the organization.

    :ivar id: The unique identifier for the employee
    :ivar dni: The national identification number of the employee (8 digits)
    :ivar paternal_surname: The paternal last name of the employee
    :ivar maternal_surname: The maternal last name of the employee
    :ivar names: The name(s) of the employee
    :ivar gender: The gender of the employee ('Male' or 'Female')
    :ivar created_at: The timestamp when the employee record was created
    :ivar updated_at: The timestamp when the employee record was last updated
    :ivar position_id: The ID of the employee's position
    :ivar department_id: The ID of the employee's department
    :ivar position: The position of the employee
    :ivar department: The department the employee belongs to
    :ivar user: The user account associated with the employee
    """

    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint(
            "dni >= 10000000 AND dni <= 99999999",
            name="ck_employee_dni_8digits",
        ),
        CheckConstraint(
            "LENGTH(paternal_surname) > 3", name="ck_employee_paternal_surname"
        ),
        CheckConstraint(
            "LENGTH(maternal_surname) > 3", name="ck_employee_maternal_surname"
        ),
        CheckConstraint("LENGTH(names) > 3", name="ck_employee_names"),
        CheckConstraint(
            "gender IN ('Male', 'Female')", name="ck_employee_gender_valid"
        ),
    )

    id: int | None = Field(None, sa_column=Column(BIGINT, primary_key=True))
    dni: int = Field(sa_column=Column(BIGINT, nullable=False, unique=True))
    paternal_surname: str = Field(sa_column=Column(TEXT, nullable=False))
    maternal_surname: str = Field(sa_column=Column(TEXT, nullable=False))
    names: str = Field(sa_column=Column(TEXT, nullable=False))
    gender: str = Field(sa_column=Column(TEXT, nullable=False))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    position_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "positions.id", name="fk_employees_position", ondelete="RESTRICT"
            ),
            nullable=False,
        )
    )
    department_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "departments.id", name="fk_employees_department", ondelete="RESTRICT"
            ),
            nullable=False,
        )
    )

    position: "Position" = Relationship(back_populates="employees")
    department: "Department" = Relationship(back_populates="employees")
    user: "User" = Relationship(back_populates="employee")
