from fastapi import HTTPException
from datetime import datetime
from .error_detail import ErrorDetail


class BaseHTTPException(HTTPException):
    """
    Base class for all custom HTTP exceptions.
    Provides consistent error formatting using ErrorDetail.
    """

    def __init__(
            self,
            type_: str,
            code: int,
            message: str,
            details: str = None,
            time: str = None
    ):
        """
        Initialize a new BaseHTTPException.

        :param type_: The type of the error
        :param code: HTTP status code
        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        """

        error = ErrorDetail(
            type=type_,
            code=code,
            message=message,
            details=details,
            time=time or datetime.now().isoformat()
        )

        super().__init__(
            status_code=code,
            detail=error.model_dump()
        )