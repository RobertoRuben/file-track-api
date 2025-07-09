from pydantic import Field
from src.app.core.exception.model import ErrorDetail


class ConflictError(ErrorDetail):
    """
    ConflictError model for handling conflict errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for server-side conflict errors, specifically 409 Conflict
    scenarios where the request could not be completed due to a conflict with
    the current state of the target resource.

    :ivar type: Type of error
    :ivar code: HTTP status code
    :ivar message: Human-readable error message
    :ivar details: Additional details about the error
    :ivar timestamp: Timestamp of when the error occurred
    """

    title: str = Field(
        default="Conflict", description="Identifies the error as a conflict error"
    )
    status: int = Field(
        default=409,
        description="HTTP 409 Conflict status code indicating that the request could not be completed due to a conflict with the current state of the target resource",
    )

    detail: str = Field(
        default="The request could not be completed due to a conflict with the current state of the target resource.",
        description="Human-readable error message",
        examples=[
            "Resource already exists.",
            "Document already exists.",
            "The requested resource is in conflict with the current state.",
        ],
    )
    details: str = Field(
        default=None,
        description="Additional details about the error",
        examples=[
            "Resource already exists with the same identifier.",
        ],
    )
