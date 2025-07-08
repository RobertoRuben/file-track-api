from .model import BaseHTTPException


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
        type_: str = "https://api.file-track/errors/forbidden",
        code: int = 403,
    ):
        """
        Initialize a new ForbiddenException.
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
