from pydantic import Field
from src.app.core.exception.model import ErrorDetail


class ForbiddenError(ErrorDetail):
    """
    ForbiddenError model for handling forbidden errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for server-side forbidden errors, specifically 403 Forbidden
    scenarios where the server understands the request but refuses to authorize it.

    :ivar type: Type of error
    :ivar code: HTTP status code
    :ivar message: Human-readable error message
    :ivar details: Additional details about the error
    :ivar timestamp: Timestamp of when the error occurred
    """

    title: str = Field(
        default="Forbidden",
        description="Identifies the error as a forbidden error",
        examples=["Permission Error", "Access Denied", "Authorization Error"],
    )
    status: int = Field(
        default=403,
        description="HTTP 403 Forbidden status code indicating that the server understands the request but refuses to authorize it",
    )
    detail: str = Field(
        default="You do not have permission to access this resource.",
        description="Human-readable error message",
        examples=[
            "You do not have permission to access this resource.",
            "Access denied to the requested resource.",
            "Authorization required for this action.",
        ],
    )
    details: str = Field(
        default=None,
        description="Additional details about the error",
        examples=[
            "User does not have the required role.",
            "Access token is missing or invalid.",
            "Resource is restricted to certain users.",
        ],
    )
