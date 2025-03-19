from pydantic import BaseModel, Field
from datetime import datetime

class ErrorDetail(BaseModel):
    """
    Error detail model for consistent error response format.
    """
    type: str = Field(..., description="The type of the error")
    code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Human-readable error message")
    details: str | None = Field(None, description="Additional details about the error")
    time: str = Field(datetime.now().isoformat(), description="Timestamp of when the error occurred")