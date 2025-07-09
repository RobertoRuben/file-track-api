from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from src.app.dto.response import CurrentUserResponseDTO
from src.app.service.interfaces import IAuthService
from src.app.service.dependencies import get_auth_service
from src.app.core.security.auth import scope_descriptions

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login", scopes=scope_descriptions
)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    auth_service: IAuthService = Depends(get_auth_service),
) -> CurrentUserResponseDTO:
    """
    Dependency that verifies the current user based on the provided token
    and checks if the required security scopes are satisfied.

    :param security_scopes: Scopes required by the endpoint
    :param token: JWT access token extracted via OAuth2PasswordBearer
    :param auth_service: The authentication service implementation
    :return: CurrentUserResponseDTO containing the current user's information
    """
    return await auth_service.get_current_user_with_scopes(
        token,
        security_scopes.scopes,
    )
