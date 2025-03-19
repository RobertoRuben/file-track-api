from .model import BaseHTTPException

class ServerException(BaseHTTPException):
    """
    Custom exception for unexpected server errors.
    Provides a standardized way to handle and report internal server errors.
    """

    def __init__(
            self,
            message: str = "An unexpected server error occurred.",
            details: str = None,
            time: str = None,
            type_: str = "Server Error",
            code: int = 500
    ):
        """
        Initialize a new ServerException.
        """
        super().__init__(
            type_=type_,
            code=code,
            message=message,
            details=details,
            time=time
        )