from fastapi import Depends
from src.app.core.security.auth.interface import IAuthService
from src.app.core.security.auth.implementations import AuthServiceImpl
from src.app.core.security.auth.dependencies import get_token_provider
from src.app.core.security.hasher.dependencies import get_hasher_provider
from src.app.domain.user.repository.dependencies import get_user_repository


async def get_auth_service(
    user_repository=Depends(get_user_repository),
    token_provider=Depends(get_token_provider),
    hasher_provider=Depends(get_hasher_provider),
) -> IAuthService:
    """
    Dependency function to obtain the authentication service implementation.

    This function creates and provides an instance of the authentication service
    (`AuthServiceImpl`) with the necessary repository and provider dependencies injected.

    :param user_repository: The user repository implementation provided by the FastAPI dependency injection system
    :param token_provider: The token provider used to generate and validate tokens
    :param hasher_provider: The hashing provider used to verify user passwords
    :return: An instance of `IAuthService` configured with the provided dependencies
    """
    return AuthServiceImpl(
        user_repository=user_repository,
        token_provider=token_provider,
        hasher_provider=hasher_provider,
    )
