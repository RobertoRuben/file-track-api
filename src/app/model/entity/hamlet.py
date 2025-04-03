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
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .settlement import Settlement


class Hamlet(SQLModel, table=True):
    """
    Represents a hamlet or small village.

    Attributes:
        id: The unique identifier for the hamlet
        name: The name of the hamlet
        created_at: The timestamp when the hamlet was created
        updated_at: The timestamp when the hamlet was last updated
        settlement_id: The ID of the settlement this hamlet belongs to
        settlement: The settlement this hamlet belongs to
    """

    __tablename__ = "hamlets"
    __table_args__ = (CheckConstraint("LENGTH(name) > 3", name="ck_hamlet_name"),)
    id: int | None = Field(default=None, sa_column=Column(BigInteger, primary_key=True))
    name: str = Field(default=None, sa_column=Column(TEXT, unique=True, nullable=False))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
    settlement_id: int | None = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "settlements.id",
                name="fk_hamlets_settlement",
                ondelete="CASCADE",
            ),
            nullable=True,
        )
    )

    settlement: Optional["Settlement"] = Relationship(back_populates="hamlets")
