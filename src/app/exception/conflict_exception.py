from .model import BaseHTTPException
from .constants import ErrorTypes, ErrorTitles


class ConflictException(BaseHTTPException):
    """
    Custom exception for conflict-related errors.
    Used when a resource already exists or there is a conflict in data operations.
    """

    def __init__(
        self,
        message: str = "A conflict occurred with the requested operation.",
        details: str = None,
        instance: str = None,
        time: str = None,
        type_: str = ErrorTypes.CONFLICT,
        title: str = ErrorTitles.CONFLICT,
        code: int = 409,
    ):
        """
        Initialize a new ConflictException.

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
