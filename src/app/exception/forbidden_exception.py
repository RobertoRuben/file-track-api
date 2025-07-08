from .model import BaseHTTPException
from .constants import ErrorTypes, ErrorTitles


class ForbiddenException(BaseHTTPException):
    """
    Custom exception for forbidden access errors.
    Used when the client does not have permission to access the requested resource.
    """

    def __init__(
        self,
        message: str = "You don't have permission to access this resource.",
        details: str = None,
        instance: str = None,
        time: str = None,
        type_: str = ErrorTypes.MISSING_PERMISSION,
        title: str = ErrorTitles.FORBIDDEN,
        headers: dict = None,
    ):
        """
        Initialize a new ForbiddenException.
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
            code=403,
            message=message,
            details=details,
            instance=instance,
            time=time,
            title=title,
            headers=headers,
        )
