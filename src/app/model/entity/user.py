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
    from .rol import Rol
    from .trabajador import Trabajador


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("LENGTH(username) > 3", name="ck_user_username"),
        CheckConstraint("LENGTH(password) >= 8", name="ck_user_password"),
    )
    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    username: str = Field(sa_column=Column(TEXT, unique=True, nullable=False))
    password: str = Field(sa_column=Column(TEXT, nullable=False))
    is_active: bool | None = Field(default=True, sa_column=Column(BOOLEAN))
    rol_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey("roles.id", name="fk_users_roles", ondelete="CASCADE"),
            nullable=False,
        )
    )
    employee_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "trabajadores.id", name="fk_users_employees", ondelete="CASCADE"
            ),
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

    role: "Rol" = Relationship(back_populates="users")
    employee: "Trabajador" = Relationship(back_populates="user")
