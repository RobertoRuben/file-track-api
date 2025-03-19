from pydantic import Field
from src.app.exception.model import ErrorDetail

class ConflictError(ErrorDetail):
    """
    ConflictError model for handling conflict errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for server-side conflict errors, specifically 409 Conflict
    scenarios where the request could not be completed due to a conflict with
    the current state of the target resource.
    """
    type: str = Field(
        default="Conflict",
        description="Identifies the error as a conflict error"
    )
    code: int = Field(
        default=409,
        description="HTTP 409 Conflict status code indicating that the request could not be completed due to a conflict with the current state of the target resource"
    )