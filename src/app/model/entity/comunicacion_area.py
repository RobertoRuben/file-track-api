from sqlmodel import (
    BIGINT,
    UniqueConstraint,
    Column,
    DateTime,
    Field,
    SQLModel,
    ForeignKey,
    text,
    Relationship,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .area import Area


class ComunicacionArea(SQLModel, table=True):
    __tablename__ = "comunicacion_areas"
    __table_args__ = (
        UniqueConstraint(
            "area_origen_id",
            "area_destino_id",
            name="uq_comunicacion_areas_area_origen_area_destino",
        ),
    )
    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    area_origen_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "areas.id",
                name="fk_comunicacion_areas_area_origen",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    area_destino_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "areas.id",
                name="fk_comunicacion_areas_area_destino",
                ondelete="CASCADE",
            ),
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

    area_origen: "Area" = Relationship(
        back_populates="comunicacion_areas_origen",
        sa_relationship_kwargs={
            "primaryjoin": "Area.id == ComunicacionArea.area_origen_id",
        },
    )
    area_destino: "Area" = Relationship(
        back_populates="comunicacion_areas_destino",
        sa_relationship_kwargs={
            "primaryjoin": "Area.id == ComunicacionArea.area_destino_id",
        },
    )
