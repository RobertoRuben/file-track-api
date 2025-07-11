from pydantic import Field
from src.app.core.exception.model import ErrorDetail


class BackRequestError(ErrorDetail):
    """
    BackRequestResponse model for handling bad request errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for client-side request errors, specifically 400 Bad Request
    scenarios where the server cannot process the request due to client error
    (malformed request syntax, invalid request message framing, or deceptive
    request routing).

    :ivar code: HTTP status code
    :ivar type: Type of error
    :ivar message: Human-readable error message
    :ivar details: Additional details about the error
    :ivar timestamp: Timestamp of when the error occurred
    """

    title: str = Field(
        default="Back Request",
        description="Identifies the error as a client-side request error",
    )
    status: int = Field(
        default=400,
        description="HTTP 400 Bad Request status code indicating that the server cannot process the request due to client error",
    )
    detail: str = Field(
        default="The request contains invalid parameters.",
        description="Human-readable error message",
        examples=[
            "The request contains invalid parameters.",
            "The request is malformed or contains invalid syntax.",
            "The request cannot be fulfilled due to bad syntax.",
        ],
    )

    details: str = Field(
        default=None,
        description="Additional details about the error",
        examples=[
            "Missing required parameters.",
            "Invalid data format in the request body.",
            "Unsupported media type in the request headers.",
        ],
    )
