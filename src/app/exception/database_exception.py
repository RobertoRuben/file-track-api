from .model import BaseHTTPException


class DatabaseException(BaseHTTPException):
    """
    Custom exception for database errors.
    Used when an error occurs in the database.
    """

    def __init__(
        self,
        message: str = "An error occurred in the database.",
        details: str = None,
        time: str = None,
        type_: str = "Database Error",
        code: int = 500,
    ):
        """
        Initialize a new DatabaseException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: The type of the error
        :param code: HTTP status code
        """
        super().__init__(
            type_=type_, code=code, message=message, details=details, time=time
        )
