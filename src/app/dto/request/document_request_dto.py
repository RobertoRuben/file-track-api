from pydantic import BaseModel, Field


class DocumentRequestDTO(BaseModel):
    """
    DTO for creating or updating a document.

    :ivar title: Document's title. Must be longer than 3 characters
    :ivar subject: Document's subject. Must be longer than 3 characters
    :ivar pages: Number of pages in the document. Must be greater than 0
    :ivar document: Binary content of the document
    :ivar submitter_id: ID of the submitter of the document
    :ivar document_category_id: ID of the document category
    :ivar documentary_topic_id: ID of the documentary topic associated with the document
    :ivar hamlet_id: Optional ID of the hamlet related to the document
    :ivar settlement_id: ID of the settlement associated with the document
    """

    title: str = Field(
        ...,
        description="Document's title. Must be longer than 3 characters and unique.",
        examples=["Annual Budget Report 2023", "Environmental Impact Assessment"],
    )
    subject: str = Field(
        ...,
        description="Document's subject or brief description. Must be longer than 3 characters.",
        examples=[
            "Financial planning for fiscal year",
            "Analysis of project effects on local ecosystem",
        ],
    )
    pages: int = Field(
        ...,
        description="Number of pages in the document. Must be greater than 0.",
        gt=0,
        examples=[12, 45],
    )
    document: bytes | None = Field(
        default=None, description="Binary content of the document file."
    )
    submitter_id: int = Field(
        ...,
        description="ID of the person or entity submitting the document.",
        examples=[1, 342],
    )
    document_category_id: int = Field(
        ..., description="ID of the category this document belongs to.", examples=[2, 7]
    )
    documentary_topic_id: int = Field(
        ...,
        description="ID of the documentary topic associated with this document.",
        examples=[5, 12],
    )
    hamlet_id: int | None = Field(
        None,
        description="Optional ID of the hamlet related to this document, if applicable.",
        examples=[None, 3],
    )
    settlement_id: int = Field(
        ...,
        description="ID of the settlement associated with this document.",
        examples=[8, 15],
    )
