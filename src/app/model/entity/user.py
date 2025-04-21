from sqlmodel import (
    text,
    BIGINT,
    TEXT,
    BOOLEAN,
    CheckConstraint,
    Column,
    DateTime,
    Field,
    SQLModel,
    ForeignKey,
    Relationship,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role
    from .employee import Employee
    from .document import Document


class User(SQLModel, table=True):
    """
    Represents a user of the system.

    :ivar id: The unique identifier for the user
    :ivar username: The username used for login, must be longer than 3 characters
    :ivar password: The hashed password for the user, must be at least 8 characters
    :ivar is_active: Whether the user account is active or not
    :ivar role_id: The ID of the role assigned to the user
    :ivar employee_id: The ID of the employee associated with the user
    :ivar created_at: The timestamp when the user was created
    :ivar updated_at: The timestamp when the user was last updated
    :ivar role: The role assigned to the user, relationship to Role entity
    :ivar employee: The employee associated with the user, relationship to Employee entity
    """

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("LENGTH(username) > 3", name="ck_user_username"),
        CheckConstraint("LENGTH(password) >= 8", name="ck_user_password"),
    )
    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    username: str = Field(sa_column=Column(TEXT, unique=True, nullable=False))
    password: str = Field(sa_column=Column(TEXT, nullable=False))
    is_active: bool | None = Field(default=True, sa_column=Column(BOOLEAN))
    role_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey("roles.id", name="fk_users_roles", ondelete="CASCADE"),
            nullable=False,
        )
    )
    employee_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey("employees.id", name="fk_users_employees", ondelete="CASCADE"),
            unique=True,
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

    role: "Role" = Relationship(back_populates="users")
    employee: "Employee" = Relationship(back_populates="user")
    documents: list["Document"] = Relationship(back_populates="registered_by_user")
