from src.app.security.auth.interface import ITokenProvider
from src.app.security.auth.implementations import TokenProviderImpl


async def get_token_provider() -> ITokenProvider:
    """
    Dependency function to get the token provider implementation.

    This function creates and provides an instance of the token provider
    implementation for JWT token generation and verification.

    :return: An implementation of ITokenProvider configured with default parameters
    """
    return TokenProviderImpl()
