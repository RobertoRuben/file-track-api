import jwt
from datetime import datetime, timedelta, timezone
from jwt import PyJWTError
from typing import Any
from src.app.exception import UnauthorizedException
from src.app.security.auth.interface import ITokenProvider

SECRET_KEY = "e88731089b8fdcc5539e5f9017dc7d83bcfaf38367fd777caaa5e69f63bd935f"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class TokenProviderImpl(ITokenProvider):
    def __init__(
        self,
        secret_key: str = SECRET_KEY,
        algorithm: str = ALGORITHM,
        access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS,
    ):
        """
        Initialize the TokenProvider with configuration parameters.

        :param secret_key: Secret key for JWT encoding/decoding
        :param algorithm: Algorithm used for JWT
        :param access_token_expire_minutes: Access token expiration time in minutes
        :param refresh_token_expire_days: Refresh token expiration time in days
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    async def generate_access_token(self, data: dict[str, Any]) -> str:
        """
        Generate a JWT access token with expiration.

        :param data: Data to encode in the token
        :return: Encoded JWT token
        """
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_token_expire_minutes
        )
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def generate_refresh_token(self, data: dict[str, Any]) -> str:
        """
        Generate a JWT refresh token with longer expiration.

        :param data: Data to encode in the token
        :return: Encoded JWT refresh token
        """
        expire = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_token_expire_days
        )
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def verify_and_decode_token(self, token: str) -> dict[str, Any]:
        """
        Verifies and decodes a JWT token.

        :param token: JWT token to decode
        :return: Decoded token payload
        :raises UnauthorizedException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except PyJWTError:
            raise UnauthorizedException(
                message="Invalid or expired token",
                details="Authentication failed due to an invalid or expired JWT token.",
            )
