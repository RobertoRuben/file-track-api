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
    from .area import Area
    from .cargo import Cargo


class Trabajador(SQLModel, table=True):
    __tablename__ = "trabajadores"
    __table_args__ = (
        CheckConstraint(
            "dni >= 10000000 AND dni <= 99999999", name="ck_trabajador_dni_8digitos"
        ),
        CheckConstraint(
            "LENGTH(apellido_paterno) > 3", name="ck_trabajador_apellido_paterno"
        ),
        CheckConstraint(
            "LENGTH(apellido_materno) > 3", name="ck_trabajador_apellido_materno"
        ),
        CheckConstraint("LENGTH(nombres) > 3", name="ck_trabajador_nombres"),
        CheckConstraint(
            "genero IN ('Masculino', 'Femenino')", name="ck_trabajador_genero_valido"
        ),
    )

    id: int | None = Field(None, sa_column=Column(BIGINT, primary_key=True))
    dni: int = Field(sa_column=Column(BIGINT, nullable=False, unique=True))
    apellido_paterno: str = Field(sa_column=Column(TEXT, nullable=False))
    apellido_materno: str = Field(sa_column=Column(TEXT, nullable=False))
    nombres: str = Field(sa_column=Column(TEXT, nullable=False))
    genero: str = Field(sa_column=Column(TEXT, nullable=False))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    cargo_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey("cargos.id", name="fk_trabajadores_cargo", ondelete="RESTRICT"),
            nullable=False,
        )
    )
    area_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey("areas.id", name="fk_trabajadores_areas", ondelete="RESTRICT"),
            nullable=False,
        )
    )

    cargo: "Cargo" = Relationship(back_populates="trabajadores")
    area: "Area" = Relationship(back_populates="trabajadores")
