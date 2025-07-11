from sqlmodel import (
    SQLModel,
    text,
    Field,
    CheckConstraint,
    Column,
    BIGINT,
    TEXT,
    DateTime,
    Relationship,
)
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app.domain.document.model import Document


class DocumentCategory(SQLModel, table=True):
    """
    Represents a document category in the system.

    :ivar id: The unique identifier for the document category
    :ivar name: The name of the document category
    :ivar created_at: The timestamp when the document category was created
    :ivar updated_at: The timestamp when the document category was last updated
    """

    __tablename__ = "document_categories"
    __table_args__ = (
        CheckConstraint("LENGTH(name) > 3", name="ck_document_category_name"),
    )

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

    documents: list["Document"] = Relationship(back_populates="document_category")
