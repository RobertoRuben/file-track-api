from .model import BaseHTTPException


class NotFoundException(BaseHTTPException):
    """
    Custom exception for not found errors.
    Used when a resource is not found in the database.
    """

    def __init__(
        self,
        message: str = "The requested resource was not found.",
        details: str = None,
        time: str = None,
        type_: str = "Not Found Error",
        code: int = 404,
    ):
        """
        Initialize a new NotFoundException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: The type of the error
        :param code: HTTP status code
        """
        super().__init__(
            type_=type_, code=code, message=message, details=details, time=time
        )
