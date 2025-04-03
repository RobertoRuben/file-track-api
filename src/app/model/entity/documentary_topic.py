from sqlmodel import (
    SQLModel,
    text,
    Field,
    CheckConstraint,
    Column,
    BIGINT,
    TEXT,
    DateTime,
)
from datetime import datetime


class DocumentaryTopic(SQLModel, table=True):
    """
    Represents a documentary topic or scope in the system.

    Attributes:
        id: The unique identifier for the documentary topic
        name: The name of the documentary topic
        created_at: The timestamp when the topic was created
        updated_at: The timestamp when the topic was last updated
    """

    __tablename__ = "documentary_topics"
    __table_args__ = (CheckConstraint("LENGTH(name) > 3", name="ck_topic_name"),)

    id: int | None = Field(default=None, sa_column=Column(BIGINT, primary_key=True))
    name: str = Field(sa_column=Column(TEXT, nullable=False, unique=True))
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP")
        ),
    )
    updated_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True))
    )
