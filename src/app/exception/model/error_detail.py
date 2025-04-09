from pydantic import BaseModel, Field
from datetime import datetime


class ErrorDetail(BaseModel):
    """
    Error detail model for consistent error response format.

    This model is used to provide a standardized response format for errors
    :ivar type: str: The type of the error
    :ivar code: int: HTTP status code
    :ivar message: str: The error message
    :ivar details: str: Additional details about the error
    :ivar time: str: Timestamp of when the error occurred
    """

    type: str = Field(..., description="The type of the error")
    code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Human-readable error message")
    details: str | None = Field(
        default=None, description="Additional details about the error"
    )
    time: str = Field(
        datetime.now().isoformat(), description="Timestamp of when the error occurred"
    )
