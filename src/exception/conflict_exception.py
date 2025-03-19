from .model import BaseHTTPException


class ConflictException(BaseHTTPException):
    """
    Custom exception for conflict-related errors.
    Used when a resource already exists or there is a conflict in data operations.
    """

    def __init__(
            self,
            message: str = "A conflict occurred with the requested operation.",
            details: str = None,
            time: str = None,
            type_: str = "Conflict Error",
            code: int = 409
    ):
        """
        Initialize a new ConflictException.
        """
        super().__init__(
            type_=type_,
            code=code,
            message=message,
            details=details,
            time=time
        )