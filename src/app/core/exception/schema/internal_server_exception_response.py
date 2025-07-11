from pydantic import Field
from src.app.core.exception.model import ErrorDetail


class InternalServerError(ErrorDetail):
    """
    InternalServerError model for handling internal server errors (HTTP 500).

    This class extends the base ErrorDetail model to provide a standardized
    response format for unexpected server-side errors. It represents situations
    where the server encountered an unexpected condition or exception that
    prevented it from fulfilling the legitimate request, requiring no action
    from the client as the issue is server-related.

    :ivar type: Type of error
    :ivar code: HTTP status code
    :ivar message: Human-readable error message
    :ivar details: Additional details about the error
    :ivar timestamp: Timestamp of when the error occurred
    """

    title: str = Field(
        default="Internal Server Error",
        description="Error classification identifying a server-side unexpected failure",
    )
    status: int = Field(
        default=500,
        description="HTTP status code 500 indicating the server encountered an unexpected condition preventing request fulfillment",
    )
    detail: str = Field(
        default="The server encountered an unexpected condition that prevented it from fulfilling the request.",
        description="Human-readable error message",
        examples=[
            "An unexpected error occurred on the server.",
            "The server encountered an internal error.",
            "An unexpected condition was encountered.",
        ],
    )
    details: str | None = Field(
        default=None,
        description="Additional details about the error",
        examples=[
            "Database connection failed.",
            "Unexpected exception occurred during processing.",
            "Server misconfiguration detected.",
        ],
    )
