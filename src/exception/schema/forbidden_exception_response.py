from pydantic import Field
from src.exception.model import ErrorDetail

class ForbiddenError(ErrorDetail):
    """
    ForbiddenError model for handling forbidden errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for server-side forbidden errors, specifically 403 Forbidden
    scenarios where the server understands the request but refuses to authorize it.
    """
    type: str = Field(
        default="Forbidden",
        description="Identifies the error as a forbidden error"
    )
    code: int = Field(
        default=403,
        description="HTTP 403 Forbidden status code indicating that the server understands the request but refuses to authorize it"
    )