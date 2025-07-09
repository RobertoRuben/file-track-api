from .model import BaseHTTPException
from .constants import ErrorTypes, ErrorTitles


class NotFoundException(BaseHTTPException):
    """
    Custom exception for not found errors.
    Used when a resource is not found in the database.
    """

    def __init__(
        self,
        message: str = "The requested resource was not found.",
        details: str = None,
        instance: str = None,
        time: str = None,
        type_: str = ErrorTypes.NOT_FOUND,
        title: str = ErrorTitles.NOT_FOUND,
        code: int = 404,
    ):
        """
        Initialize a new NotFoundException.

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
