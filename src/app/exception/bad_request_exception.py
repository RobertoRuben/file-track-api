from .model import BaseHTTPException
from .constants import ErrorTypes, ErrorTitles


class BadRequestException(BaseHTTPException):
    """
    Custom exception for bad request errors.
    Used when the client sends invalid or malformed data.
    """

    def __init__(
        self,
        message: str = "The request contains invalid parameters.",
        details: str = None,
        instance: str = None,
        time: str = None,
        type_: str = ErrorTypes.BAD_REQUEST,
        title: str = ErrorTitles.BAD_REQUEST,
        code: int = 400,
    ):
        """
        Initialize a new BadRequestException.

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
