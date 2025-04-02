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


class Rol(SQLModel, table=True):
    __tablename__ = "roles"
    __table_args__ = (CheckConstraint("LENGTH(nombre) > 3", name="ck_rol_name"),)

    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    nombre: str = Field(sa_column=Column(TEXT, nullable=False, unique=True))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    users: list["User"] = Relationship(back_populates="role")
