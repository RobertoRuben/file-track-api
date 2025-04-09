from .model import BaseHTTPException


class ConflictException(BaseHTTPException):
    """
    Custom exception for conflict-related errors.
    Used when a resource already exists or there is a conflict in data operations.
    """

    def __init__(
        self,
        message: str = "A conflict occurred with the requested operation.",
        details: str = None,
        time: str = None,
        type_: str = "Conflict Error",
        code: int = 409,
    ):
        """
        Initialize a new ConflictException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: The type of the error
        :param code: HTTP status code
        """
        super().__init__(
            type_=type_, code=code, message=message, details=details, time=time
        )
