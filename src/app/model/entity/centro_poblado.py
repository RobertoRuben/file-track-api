from sqlmodel import (
    SQLModel,
    text,
    BIGINT,
    Field,
    CheckConstraint,
    Column,
    TEXT,
    DateTime,
)
from datetime import datetime


class CentroPoblado(SQLModel, table=True):
    __tablename__ = "centros_poblados"
    __table_args__ = (
        CheckConstraint("LENGTH(nombre) > 3", name="ck_centro_poblado_name"),
        CheckConstraint("LENGTH(nombre) < 100", name="ck_centro_poblado_name_length"),
    )
    id: int | None = Field(None, sa_column=Column(BIGINT, primary_key=True))
    nombre: str = Field(sa_column=Column(TEXT, nullable=False, unique=True))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
