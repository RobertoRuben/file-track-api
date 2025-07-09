from .model import BaseHTTPException
from .constants import ErrorTypes, ErrorTitles


class InvalidFieldException(BaseHTTPException):
    """
    Custom exception for invalid field errors.
    Used when a field provided doesn't exist in the model.
    """

    def __init__(
        self,
        message: str = "Invalid field provided.",
        details: str = None,
        instance: str = None,
        time: str = None,
        type_: str = ErrorTypes.INVALID_FIELD,
        title: str = ErrorTitles.BAD_REQUEST,
        code: int = 400,
    ):
        """
        Initialize a new InvalidFieldException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param instance: URI that identifies the specific occurrence of the problem
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: URI that identifies the problem type
        :param title: A short, human-readable summary of the problem type
        :param code: HTTP status code
        """
        super().__init__(
            type_=type_,
            code=code,
            message=message,
            details=details,
            instance=instance,
            time=time,
            title=title,
        )
