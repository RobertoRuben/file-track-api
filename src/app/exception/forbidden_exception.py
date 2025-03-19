from .model import BaseHTTPException


class ForbiddenException(BaseHTTPException):
    """Exception for forbidden access (403)."""

    def __init__(
            self,
            message: str = "You don't have permission to access this resource.",
            details: str = None,
            time: str = None
    ):
        super().__init__(
            type_="Permission Error",
            code=403,
            message=message,
            details=details,
            time=time
        )