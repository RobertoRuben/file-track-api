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


class Remitente(SQLModel, table=True):
    __tablename__ = "remitentes"
    __table_args__ = (
        CheckConstraint(
            "LENGTH(apellido_paterno) > 3", name="ck_remitente_apellido_paterno"
        ),
        CheckConstraint(
            "LENGTH(apellido_materno) > 3", name="ck_remitente_apellido_materno"
        ),
        CheckConstraint("LENGTH(nombres) > 3", name="ck_remitente_nombres"),
        CheckConstraint(
            "dni >= 10000000 AND dni <= 99999999", name="ck_remitente_dni_range"
        ),
        CheckConstraint(
            "genero IN ('Masculino', 'Femenino')", name="ck_remitente_genero_values"
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
