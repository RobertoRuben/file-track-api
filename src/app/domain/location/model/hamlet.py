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
    from src.app.domain.location.model import Settlement
    from src.app.domain.document.model import Document


class Hamlet(SQLModel, table=True):
    """
    Represents a hamlet or small village.

    :ivar id: The unique identifier for the hamlet
    :ivar name: The name of the hamlet
    :ivar created_at: The timestamp when the hamlet was created
    :ivar updated_at: The timestamp when the hamlet was last updated
    :ivar settlement_id: The ID of the settlement this hamlet belongs to
    :ivar settlement: The settlement this hamlet belongs to
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
    documents: list["Document"] = Relationship(back_populates="hamlet")
