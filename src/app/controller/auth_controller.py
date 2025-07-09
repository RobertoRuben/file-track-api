from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from src.app.core.exception.schema import (
    BackRequestError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
)
from src.app.dto.request import AuthRequestDTO
from src.app.dto.response import (
    AuthResponseDTO,
    CurrentUserResponseDTO,
)
from src.app.service.interfaces import IAuthService
from src.app.service.dependencies import get_auth_service, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_tags_metadata = {
    "name": "Authentication",
    "description": "Comprehensive authentication and authorization management system providing secure user access control "
    "and session management. Handles credential validation, JWT token generation and refresh, user identity "
    "verification, and secure session continuity. Essential security layer ensuring only authorized users "
    "can access protected resources while maintaining seamless user experience through advanced token management "
    "and automated session handling for enterprise-grade security compliance.",
}


@router.post(
    "/login",
    response_model=AuthResponseDTO,
    summary="Authenticate user and generate tokens",
    responses={
        200: {
            "model": AuthResponseDTO,
            "description": "Authentication successful",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Invalid credentials"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Authenticates users with secure credential validation and generates JWT token pairs for authorized "
    "system access. Validates username and password against the user database, enforces security policies, "
    "and provides both access tokens for immediate resource access and refresh tokens for session continuity.",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: IAuthService = Depends(get_auth_service),
) -> AuthResponseDTO:
    """
    Endpoint to authenticate users and generate authentication tokens.

    This endpoint receives user credentials (username and password), validates them,
    and if valid, returns access and refresh tokens for the user. The access token
    allows the user to access protected resources, while the refresh token can be used
    to obtain a new access token when the current one expires.

    :param form_data: Form containing username and password for authentication.
    :param auth_service: Service that handles the authentication logic.
    :return: Authentication response containing access and refresh tokens.
    """
    auth_request = AuthRequestDTO(
        username=form_data.username,
        password=form_data.password,
    )
    return await auth_service.authenticate(auth_request)


@router.post(
    "/refresh",
    response_model=AuthResponseDTO,
    summary="Refresh access token",
    responses={
        200: {
            "model": AuthResponseDTO,
            "description": "Token refreshed successfully",
        },
        400: {"model": BackRequestError, "description": "Bad request error"},
        401: {"model": UnauthorizedError, "description": "Invalid refresh token"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Generates new access tokens using valid refresh tokens for seamless session management without "
    "credential re-entry. Validates refresh token authenticity, checks expiration status, and issues fresh "
    "access tokens while maintaining security boundaries and user session continuity for enhanced user experience.",
)
async def refresh_token(
    refresh_token: str,
    auth_service: IAuthService = Depends(get_auth_service),
) -> AuthResponseDTO:
    """
    Endpoint to refresh an access token using a refresh token.

    This endpoint allows a user to obtain a new access token by providing a valid
    refresh token. This is typically used when the original access token has expired
    but the user wishes to maintain their authenticated session without logging in again.

    :param refresh_token: The refresh token used to generate a new access token.
    :param auth_service: Service that handles the token refresh logic.
    :return: Authentication response containing new access token and the existing refresh token.
    """
    return await auth_service.generate_refresh_access_token(refresh_token)


@router.get(
    "/me",
    response_model=CurrentUserResponseDTO,
    summary="Get current authenticated user",
    responses={
        200: {
            "model": CurrentUserResponseDTO,
            "description": "Current user information",
        },
        401: {"model": UnauthorizedError, "description": "Not authenticated"},
        404: {"model": NotFoundError, "description": "User not found"},
        500: {"model": InternalServerError, "description": "Internal server error"},
    },
    description="Retrieves comprehensive profile information of the currently authenticated user including personal "
    "details, role assignments, and system permissions. Validates bearer token authenticity, extracts user "
    "identity securely, and provides complete user context for client applications and user profile management.",
)
async def get_user_me(
    current_user: CurrentUserResponseDTO = Depends(get_current_user),
) -> CurrentUserResponseDTO:
    """
    Endpoint to retrieve the current authenticated user's information.

    This endpoint returns the profile information of the currently authenticated user.
    It uses the access token provided in the Authorization header to identify and
    return the appropriate user data.

    :param current_user: The authenticated user retrieved from the bearer token.
    :return: User information of the currently authenticated user.
    """
    return current_user
