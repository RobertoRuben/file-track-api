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
    from .trabajador import Trabajador


class Area(SQLModel, table=True):
    __tablename__ = "areas"
    __table_args__ = (CheckConstraint("LENGTH(nombre) > 3", name="ck_area_name"),)

    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    nombre: str = Field(default=None, sa_column=Column(TEXT, unique=True))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    trabajadores: list["Trabajador"] = Relationship(back_populates="area")
