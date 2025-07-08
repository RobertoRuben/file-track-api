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
        instance: str = None,
        time: str = None,
        type_: str = "https://api.file-track/errors/database-error",
        code: int = 500,
    ):
        """
        Initialize a new DatabaseException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param instance: URI that identifies the specific occurrence of the problem
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: URI that identifies the problem type
        :param code: HTTP status code
        """
        super().__init__(
            type_=type_,
            code=code,
            message=message,
            details=details,
            instance=instance,
            time=time,
        )
