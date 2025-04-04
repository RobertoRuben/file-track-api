from sqlmodel import (
    SQLModel,
    text,
    BIGINT,
    Field,
    CheckConstraint,
    Column,
    TEXT,
    DateTime,
    Relationship,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .hamlet import Hamlet


class Settlement(SQLModel, table=True):
    """
    Represents a settlement or populated center.

    :ivar id: The unique identifier for the settlement
    :ivar name: The name of the settlement
    :ivar created_at: The timestamp when the settlement was created
    :ivar updated_at: The timestamp when the settlement was last updated
    :ivar hamlets: List of hamlets that belong to this settlement
    """

    __tablename__ = "settlements"
    __table_args__ = (
        CheckConstraint("LENGTH(name) > 3", name="ck_settlement_name"),
        CheckConstraint("LENGTH(name) < 100", name="ck_settlement_name_length"),
    )
    id: int | None = Field(None, sa_column=Column(BIGINT, primary_key=True))
    name: str = Field(sa_column=Column(TEXT, nullable=False, unique=True))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )

    hamlets: list["Hamlet"] = Relationship(back_populates="settlement")
