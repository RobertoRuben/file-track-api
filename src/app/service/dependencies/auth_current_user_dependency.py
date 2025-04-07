from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from src.app.dto.response import UserResponseDTO
from src.app.service.interfaces import IAuthService
from src.app.service.dependencies import get_auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: IAuthService = Depends(get_auth_service),
) -> UserResponseDTO:
    """
    Dependency function to retrieve the current user from a Bearer token.

    This function extracts the token using `oauth2_scheme` and calls
    `auth_service.get_current_user(token)` to validate and decode the token.
    If the token is valid, it returns a `UserResponseDTO` with the authenticated user's data.
    Otherwise, it raises a 401 exception for invalid or expired tokens.

    :param token: The Bearer token extracted by the FastAPI dependency injection system
    :param auth_service: The authentication service used to validate the token and retrieve the current user
    :return: A `UserResponseDTO` containing the information of the authenticated user
    """
    return await auth_service.get_current_user(token)
