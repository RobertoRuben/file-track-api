from .model import BaseHTTPException


class UnauthorizedException(BaseHTTPException):
    """Exception for unauthorized access (401)."""

    def __init__(
        self,
        message: str = "Authentication credentials are missing or invalid.",
        details: str = None,
        time: str = None,
        headers: dict = None,
    ):
        super().__init__(
            message=message,
            code=401,
            type_="Authentication Error",
            details=details,
            time=time,
            headers=headers,
        )
