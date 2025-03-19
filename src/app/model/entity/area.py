from sqlmodel import (
    SQLModel,
    text,
    Field,
    CheckConstraint,
    Column,
    BIGINT,
    TEXT,
    DateTime
)
from datetime import datetime

class Area(SQLModel, table=True):
    __tablename__ = "areas"
    __table_args__ = (
        CheckConstraint("LENGTH(nombre) > 3", name="ck_area_name"),
    )

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