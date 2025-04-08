from pydantic import Field
from src.app.exception.model import ErrorDetail


class UnauthorizedError(ErrorDetail):
    """
    UnauthorizedError model for handling authentication failures.

    This class extends the base ErrorDetail model to provide a standardized
    response format for authentication errors, specifically 401 Unauthorized
    scenarios where the request lacks valid authentication credentials or
    the provided credentials are invalid.

    :ivar type: Type of error
    :ivar code: HTTP status code
    :ivar message: Human-readable error message
    :ivar details: Additional details about the error
    :ivar time: Timestamp of when the error occurred
    """

    type: str = Field(
        default="Unauthorized",
        description="Identifies the error as an authentication failure",
    )
    code: int = Field(
        default=401,
        description="HTTP 401 Unauthorized status code indicating that the request requires valid authentication credentials",
    )
    message: str = Field(
        default="Authentication credentials are missing or invalid.",
        description="Human-readable error message",
        examples=[
            "Authentication credentials are missing or invalid.",
            "The request requires authentication.",
            "Invalid authentication token provided.",
        ],
    )
    details: str = Field(
        default=None,
        description="Additional details about the error",
        examples=[
            "Missing or invalid API key.",
            "Invalid username or password.",
            "Token has expired or is invalid.",
        ],
    )
