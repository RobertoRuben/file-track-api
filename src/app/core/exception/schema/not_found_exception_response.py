from pydantic import Field
from src.app.core.exception.model import ErrorDetail


class NotFoundError(ErrorDetail):
    """
    NotFoundError model for handling not found errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for server-side not found errors, specifically 404 Not Found
    scenarios where the server cannot find the requested resource.

    :ivar type: Type of error
    :ivar code: HTTP status code
    :ivar message: Human-readable error message
    :ivar details: Additional details about the error
    :ivar timestamp: Timestamp of when the error occurred
    """

    title: str = Field(
        default="Not Found", description="Identifies the error as a not found error"
    )
    status: int = Field(
        default=404,
        description="HTTP 404 Not Found status code indicating that the server cannot find the requested resource",
    )
    detail: str = Field(
        default="The requested resource was not found.",
        description="Human-readable error message",
        examples=[
            "The requested resource was not found.",
            "The specified endpoint does not exist.",
            "The requested document could not be found.",
        ],
    )
    details: str = Field(
        default=None,
        description="Additional details about the error",
        examples=[
            "Resource not found.",
            "Document not found.",
            "The requested resource does not exist.",
        ],
    )
