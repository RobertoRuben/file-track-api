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
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .submitter import Submitter
    from .document_category import DocumentCategory
    from .documentary_topic import DocumentaryTopic
    from .hamlet import Hamlet
    from .settlement import Settlement
    from .user import User


class Document(SQLModel, table=True):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint(
            "LENGTH(registration_code) = 20", name="ck_document_registration_code"
        ),
        CheckConstraint("LENGTH(title) > 3", name="ck_document_title"),
        CheckConstraint("LENGTH(subject) > 3", name="ck_document_subject"),
        CheckConstraint("pages > 0", name="ck_document_pages"),
    )

    id: int | None = Field(None, sa_column=Column(BIGINT, primary_key=True))
    registration_code: str = Field(sa_column=Column(TEXT, unique=True))
    title: str = Field(sa_column=Column(TEXT, nullable=False, unique=True))
    subject: str = Field(sa_column=Column(TEXT, nullable=False))
    pages: int = Field(sa_column=Column(BIGINT, nullable=False))
    storage_path: str = Field(sa_column=Column(TEXT, nullable=False))
    size: int = Field(sa_column=Column(BIGINT, nullable=False))
    submitter_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "submitters.id", name="fk_documents_submitter", ondelete="CASCADE"
            ),
            nullable=False,
        )
    )
    document_category_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "document_categories.id",
                name="fk_documents_document_category",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    documentary_topic_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "documentary_topics.id",
                name="fk_documents_documentary_topic",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    hamlet_id: int | None = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey("hamlets.id", name="fk_documents_hamlet", ondelete="CASCADE"),
            nullable=True,
        )
    )
    settlement_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "settlements.id",
                name="fk_documents_settlement",
                ondelete="CASCADE",
            ),
            nullable=False,
        )
    )
    registered_by_user_id: int = Field(
        sa_column=Column(
            BIGINT,
            ForeignKey(
                "users.id",
                name="fk_documents_user",
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

    submitter: "Submitter" = Relationship(back_populates="documents")
    document_category: "DocumentCategory" = Relationship(back_populates="documents")
    documentary_topic: "DocumentaryTopic" = Relationship(back_populates="documents")
    hamlet: Optional["Hamlet"] = Relationship(back_populates="documents")
    settlement: "Settlement" = Relationship(back_populates="documents")
    registered_by_user: "User" = Relationship(back_populates="documents")
