from .model import BaseHTTPException


class ForbiddenException(BaseHTTPException):
    """
    Custom exception for forbidden access errors.
    Used when the client does not have permission to access the requested resource.
    """

    def __init__(
        self,
        message: str = "You don't have permission to access this resource.",
        details: str = None,
        time: str = None,
        type_: str = "Permission Error",
        code: int = 403,
    ):
        """
        Initialize a new ForbiddenException.
        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        """
        super().__init__(
            type_=type_,
            code=code,
            message=message,
            details=details,
            time=time,
        )
