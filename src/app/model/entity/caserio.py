from sqlalchemy import BigInteger
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
    ForeignKey,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .centro_poblado import CentroPoblado


class Caserio(SQLModel, table=True):
    __tablename__ = "caserios"
    __table_args__ = (CheckConstraint("LENGTH(nombre) > 3", name="ck_caserio_name"),)
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True))
    nombre: str = Field(
        default=None, sa_column=Column(TEXT, unique=True, nullable=False)
    )
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    centro_poblado_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "centros_poblados.id",
                name="fk_caserios_centro_poblados",
                ondelete="CASCADE",
            ),
        )
    )

    centro_poblado: "CentroPoblado" = Relationship(back_populates="caserios")
