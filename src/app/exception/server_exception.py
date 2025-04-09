from .model import BaseHTTPException


class ServerException(BaseHTTPException):
    """
    Custom exception for unexpected server errors.
    Provides a standardized way to handle and report internal server errors.
    """

    def __init__(
        self,
        message: str = "An unexpected server error occurred.",
        details: str = None,
        time: str = None,
        type_: str = "Server Error",
        code: int = 500,
    ):
        """
        Initialize a new ServerException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: The type of the error
        :param code: HTTP status code
        """
        super().__init__(
            type_=type_, code=code, message=message, details=details, time=time
        )
