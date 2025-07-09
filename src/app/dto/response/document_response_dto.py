from datetime import datetime
from pydantic import BaseModel, Field
from src.app.core.schema import Page


class DocumentResponseDTO(BaseModel):
    """
    DTO for representing document data in responses.

    :ivar id: Unique identifier of the document
    :ivar registration_code: Unique 20-character registration code for the document
    :ivar title: Document title
    :ivar subject: Document's subject or brief description
    :ivar pages: Number of pages in the document
    :ivar storage_path: Path where the document is stored in the system
    :ivar size: File size in bytes
    :ivar submitter_id: ID of the person or entity that submitted the document
    :ivar document_category_id: ID of the category this document belongs to
    :ivar documentary_topic_id: ID of the documentary topic associated with the document
    :ivar hamlet_id: Optional ID of the hamlet related to the document
    :ivar settlement_id: ID of the settlement associated with the document
    :ivar registered_by_user_id: ID of the user who registered the document in the system
    :ivar created_at: Timestamp when the document was created
    :ivar updated_at: Optional timestamp when the document was last updated
    """

    id: int = Field(
        ..., description="Unique identifier of the document", examples=[1, 42]
    )
    registration_code: str = Field(
        ...,
        description="Unique 20-character registration code for the document",
        examples=["DOC00000000111042025", "DOC00000000211042025"],
    )
    title: str = Field(
        ...,
        description="Document's title",
        examples=["Annual Budget Report 2023", "Environmental Impact Assessment"],
    )
    subject: str = Field(
        ...,
        description="Document's subject or brief description",
        examples=[
            "Financial planning for fiscal year",
            "Analysis of project effects on local ecosystem",
        ],
    )
    pages: int = Field(
        ..., description="Number of pages in the document", examples=[12, 45]
    )
    storage_path: str | None = Field(
        default=None,
        description="Path where the document is stored in the system",
        examples=[
            "/storage/documents/2023/12/doc123.pdf",
            "/storage/documents/2024/03/doc456.pdf",
        ],
    )
    size: int | None = Field(
        default=None, description="File size in bytes", examples=[1536000, 8192000]
    )
    submitter_id: int | None = Field(
        default=None,
        description="ID of the person or entity that submitted the document",
        examples=[1, 342],
    )
    submitter_dni: int | None = Field(
        default=None,
        description="DNI of the person or entity that submitted the document",
        examples=[12345678, 87654321],
    )
    submitter_names: str | None = Field(
        default=None,
        description="Names of the person or entity that submitted the document",
        examples=["John Doe", "Jane Smith"],
    )
    document_category_id: int | None = Field(
        default=None,
        description="ID of the category this document belongs to",
        examples=[2, 7],
    )
    document_category_name: str | None = Field(
        default=None,
        description="Name of the category this document belongs to",
        examples=["Financial Documents", "Environmental Studies"],
    )
    documentary_topic_id: int | None = Field(
        default=None,
        description="ID of the documentary topic associated with this document",
        examples=[5, 12],
    )
    documentary_topic_name: str | None = Field(
        default=None,
        description="Name of the documentary topic associated with this document",
        examples=["Budget Planning", "Environmental Regulations"],
    )
    hamlet_id: int | None = Field(
        default=None,
        description="Optional ID of the hamlet related to this document, if applicable",
        examples=[None, 3],
    )
    hamlet_name: str | None = Field(
        default=None,
        description="Optional name of the hamlet related to this document, if applicable",
        examples=[None, "Green Valley"],
    )
    settlement_id: int | None = Field(
        default=None,
        description="ID of the settlement associated with this document",
        examples=[8, 15],
    )
    settlement_name: str | None = Field(
        default=None,
        description="Name of the settlement associated with this document",
        examples=["Springfield", "Riverdale"],
    )
    registered_by_user_id: int | None = Field(
        default=None,
        description="ID of the user who registered the document in the system",
        examples=[4, 27],
    )
    registered_by_user_name: str | None = Field(
        default=None,
        description="Name of the user who registered the document in the system",
        examples=["AJohnson45", "JDoe2645"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the document was created",
        examples=["2023-12-15T14:30:45.123Z"],
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Optional timestamp when the document was last updated",
        examples=[None, "2024-03-27T09:15:22.456Z"],
    )


class DocumentPage(Page):
    """
    DTO for paginated document responses.
    Represents a paginated collection of document data.

    :ivar data: List of documents in the current page
    """

    data: list[DocumentResponseDTO]
