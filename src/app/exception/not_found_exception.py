from .model import BaseHTTPException


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
        type_: str = "https://api.file-track/errors/not-found",
        code: int = 404,
    ):
        """
        Initialize a new NotFoundException.

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
