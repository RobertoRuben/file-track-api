from .model import BaseHTTPException
from .constants import ErrorTypes, ErrorTitles


class UnauthorizedException(BaseHTTPException):
    """
    Custom exception for unauthorized access errors.
    Used when authentication credentials are missing or invalid.
    """

    def __init__(
        self,
        message: str = "Authentication credentials are missing or invalid.",
        details: str = None,
        instance: str = None,
        time: str = None,
        type_: str = ErrorTypes.INVALID_TOKEN,
        title: str = ErrorTitles.UNAUTHORIZED,
        headers: dict = None,
    ):
        """
        Initialize a new UnauthorizedException.

        :param message: Human-readable error message
        :param details: Additional details about the error
        :param instance: URI that identifies the specific occurrence of the problem
        :param time: Timestamp when the error occurred, defaults to current time
        :param type_: URI that identifies the problem type
        :param title: A short, human-readable summary of the problem type
        :param headers: Additional headers to include in the response
        """
        super().__init__(
            type_=type_,
            code=401,
            message=message,
            details=details,
            instance=instance,
            time=time,
            title=title,
            headers=headers,
        )
