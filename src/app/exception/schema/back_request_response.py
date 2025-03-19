from pydantic import Field
from src.app.exception.model import ErrorDetail


class BackRequestError(ErrorDetail):
    """
    BackRequestResponse model for handling bad request errors.

    This class extends the base ErrorDetail model to provide a standardized
    response format for client-side request errors, specifically 400 Bad Request
    scenarios where the server cannot process the request due to client error
    (malformed request syntax, invalid request message framing, or deceptive
    request routing).
    """
    type: str = Field(
        default="Back Request",
        description="Identifies the error as a client-side request error"
    )
    code: int = Field(
        default=400,
        description="HTTP 400 Bad Request status code indicating that the server cannot process the request due to client error"
    )