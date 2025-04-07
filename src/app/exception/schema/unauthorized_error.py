from pydantic import Field
from src.app.exception.model import ErrorDetail


class UnauthorizedError(ErrorDetail):
    """
    UnauthorizedError model for handling authentication failures.

    This class extends the base ErrorDetail model to provide a standardized
    response format for authentication errors, specifically 401 Unauthorized
    scenarios where the request lacks valid authentication credentials or
    the provided credentials are invalid.
    """

    type: str = Field(
        default="Unauthorized",
        description="Identifies the error as an authentication failure",
    )
    code: int = Field(
        default=401,
        description="HTTP 401 Unauthorized status code indicating that the request requires valid authentication credentials",
    )
