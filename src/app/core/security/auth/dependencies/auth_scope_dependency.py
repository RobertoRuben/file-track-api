from fastapi import Depends
from typing import List
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dependencies import get_current_user
from src.app.core.exception import ForbiddenException


async def get_token_scopes(
    current_user: CurrentUser = Depends(get_current_user),
) -> List[str]:
    """
    Extracts the current token's scopes from the '_token_payload' attribute
    within the CurrentUserResponseDTO.

    :param current_user: The authenticated current user including the token payload
    :return: A list of scopes retrieved from the token
    """
    token = current_user.__dict__.get("_token_payload", {})
    return token.get("scopes", [])


async def requires_scopes(required_scopes: List[str]):
    """
    Dependency that checks whether the current user has the required scopes
    to access a protected endpoint.

    :param required_scopes: List of scopes required to access the endpoint
    """

    async def scope_checker(scopes: List[str] = Depends(get_token_scopes)):
        has_permission = any(scope in scopes for scope in required_scopes)

        if not has_permission:
            raise ForbiddenException(
                details="You do not have the required permissions to access this resource.",
            )

    return scope_checker
