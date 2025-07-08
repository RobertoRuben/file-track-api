from .model import BaseHTTPException


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
        type_: str = "https://api.file-track/errors/bad-request",
        code: int = 400,
    ):
        """
        Initialize a new BadRequestException.

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
