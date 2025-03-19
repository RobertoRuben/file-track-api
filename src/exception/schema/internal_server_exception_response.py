from pydantic import Field
from src.exception.model import ErrorDetail

class InternalServerError(ErrorDetail):
    """
    InternalServerError model for handling internal server errors (HTTP 500).

    This class extends the base ErrorDetail model to provide a standardized
    response format for unexpected server-side errors. It represents situations
    where the server encountered an unexpected condition or exception that
    prevented it from fulfilling the legitimate request, requiring no action
    from the client as the issue is server-related.
    """
    type: str = Field(
        default="Internal Server Error",
        description="Error classification identifying a server-side unexpected failure"
    )
    code: int = Field(
        default=500,
        description="HTTP status code 500 indicating the server encountered an unexpected condition preventing request fulfillment"
    )