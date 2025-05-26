from abc import ABC, abstractmethod
from typing import Any


class ITokenProvider(ABC):
    """
    Interface for JWT token generation and validation.
    Defines the contract for authentication token operations.
    """

    @abstractmethod
    async def generate_access_token(self, data: dict[str, Any]) -> tuple[str, int]:
        """
        Generates a JWT access token with expiration time.

        :param data: Data to encode in the token
        :return: Encoded JWT token
        """
        pass

    @abstractmethod
    async def generate_refresh_token(self, data: dict[str, Any]) -> str:
        """
        Generates a JWT refresh token with extended expiration time.

        :param data: Data to encode in the token
        :return: Encoded JWT refresh token
        """
        pass

    @abstractmethod
    async def verify_and_decode_token(self, token: str) -> dict[str, Any]:
        """
        Verifies and decodes a JWT token.

        :param token: JWT token to decode
        :return: Decoded token payload
        :raises UnauthorizedException: If token is invalid or expired
        """
        pass
