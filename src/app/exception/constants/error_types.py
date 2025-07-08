import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.file-track")
ERROR_TYPE_BASE_URL = f"{API_BASE_URL}/errors"


class ErrorTypes:
    """
    Constants for error types used in exceptions.
    These types follow the URL format according to the RFC standard for HTTP errors.
    """

    AUTHENTICATION_FAILED = f"{ERROR_TYPE_BASE_URL}/authentication-failed"
    INACTIVE_ACCOUNT = f"{ERROR_TYPE_BASE_URL}/inactive-account"
    INVALID_TOKEN = f"{ERROR_TYPE_BASE_URL}/invalid-token"
    INVALID_REFRESH_TOKEN = f"{ERROR_TYPE_BASE_URL}/invalid-refresh-token"
    USER_NOT_FOUND = f"{ERROR_TYPE_BASE_URL}/user-not-found"
    MISSING_PERMISSION = f"{ERROR_TYPE_BASE_URL}/missing-permission"

    BAD_REQUEST = f"{ERROR_TYPE_BASE_URL}/bad-request"
    NOT_FOUND = f"{ERROR_TYPE_BASE_URL}/not-found"
    CONFLICT = f"{ERROR_TYPE_BASE_URL}/conflict"
    FORBIDDEN = f"{ERROR_TYPE_BASE_URL}/forbidden"
    SERVER_ERROR = f"{ERROR_TYPE_BASE_URL}/server-error"
    DATABASE_ERROR = f"{ERROR_TYPE_BASE_URL}/database-error"
    VALIDATION_ERROR = f"{ERROR_TYPE_BASE_URL}/validation-error"
    IMPLEMENTATION_ERROR = f"{ERROR_TYPE_BASE_URL}/implementation-error"
    INVALID_FIELD = f"{ERROR_TYPE_BASE_URL}/invalid-field"
    HTTP_ERROR = f"{ERROR_TYPE_BASE_URL}/http-error"
