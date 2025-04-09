from .model import BaseHTTPException


class UnauthorizedException(BaseHTTPException):
    """
    Custom exception for unauthorized access errors.
    Used when authentication credentials are missing or invalid.
    """

    def __init__(
        self,
        message: str = "Authentication credentials are missing or invalid.",
        details: str = None,
        time: str = None,
        headers: dict = None,
    ):
        """
        Initialize a new UnauthorizedException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        :param headers: Additional headers to include in the response
        """
        super().__init__(
            message=message,
            code=401,
            type_="Authentication Error",
            details=details,
            time=time,
            headers=headers,
        )
