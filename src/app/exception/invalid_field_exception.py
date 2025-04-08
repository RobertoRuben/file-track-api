from .model import BaseHTTPException


class InvalidFieldException(BaseHTTPException):
    """
    Custom exception for invalid field errors.
    Used when a field provided doesn't exist in the model.
    """

    def __init__(
        self,
        message: str = "Invalid field provided.",
        details: str = None,
        time: str = None,
        type_: str = "Invalid Field Error",
        code: int = 400,
    ):
        """
        Initialize a new InvalidFieldException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: The type of the error
        :param code: HTTP status code
        """
        super().__init__(
            type_=type_, code=code, message=message, details=details, time=time
        )
