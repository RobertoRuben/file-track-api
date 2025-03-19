from pydantic import Field
from src.app.exception.model import ErrorDetail

class NotFoundError(ErrorDetail):
    """
    NotFoundError model for handling not found errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for server-side not found errors, specifically 404 Not Found
    scenarios where the server cannot find the requested resource.
    """
    type: str = Field(
        default="Not Found",
        description="Identifies the error as a not found error"
    )
    code: int = Field(
        default=404,
        description="HTTP 404 Not Found status code indicating that the server cannot find the requested resource"
    )