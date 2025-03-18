from .model import BaseHTTPException


class UnauthorizedException(BaseHTTPException):
    """Exception for unauthorized access (401)."""

    def __init__(
            self,
            message: str = "Authentication credentials are missing or invalid.",
            details: str = None,
            time: str = None
    ):
        super().__init__(
            type_="Authentication Error",
            code=401,
            message=message,
            details=details,
            time=time
        )