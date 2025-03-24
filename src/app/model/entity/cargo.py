from sqlmodel import (
    BIGINT,
    TEXT,
    CheckConstraint,
    Column,
    DateTime,
    Field,
    SQLModel,
    text,
)
from datetime import datetime


class Cargo(SQLModel, table=True):
    __tablename__ = "cargos"
    __table_args__ = (CheckConstraint("LENGTH(nombre) > 3", name="ck_cargo_name"),)

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
