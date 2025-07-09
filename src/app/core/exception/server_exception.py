from .model import BaseHTTPException
from .constants import ErrorTypes, ErrorTitles


class ServerException(BaseHTTPException):
    """
    Custom exception for unexpected server errors.
    Provides a standardized way to handle and report internal server errors.
    """

    def __init__(
        self,
        message: str = "An unexpected server error occurred.",
        details: str = None,
        instance: str = None,
        time: str = None,
        type_: str = ErrorTypes.SERVER_ERROR,
        title: str = ErrorTitles.INTERNAL_SERVER_ERROR,
        code: int = 500,
    ):
        """
        Initialize a new ServerException.

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
