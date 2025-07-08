from src.app.dto.request import AuthRequestDTO
from src.app.dto.response import (
    AuthResponseDTO,
    CurrentUserResponseDTO,
)
from src.app.service.interfaces import IAuthService
from src.app.repository.interfaces import IUserRepository
from src.app.security.auth.interface import ITokenProvider
from src.app.security.hasher.interface import IHasherProvider
from src.app.exception.decorator import handle_exceptions
from src.app.exception import UnauthorizedException, ForbiddenException
from src.app.security.auth.constants import Scopes
from src.app.exception.constants import ErrorTypes, ErrorTitles


class AuthServiceImpl(IAuthService):
    """
    Implementation of the IAuthService interface.

    This class is responsible for the business logic related to user authentication,
    token management, and user authorization through scope validation.

    Attributes:
        user_repository (IUserRepository): Repository for user data operations.
        token_provider (ITokenProvider): Provider for generating and validating tokens.
        hasher_provider (IHasherProvider): Provider for hashing and verifying passwords.
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        token_provider: ITokenProvider,
        hasher_provider: IHasherProvider,
    ):
        """
        Initialize the AuthServiceImpl with the required dependencies.

        Args:
            user_repository (IUserRepository): Repository instance for user data operations.
            token_provider (ITokenProvider): Token provider instance for generating and validating tokens.
            hasher_provider (IHasherProvider): Hasher provider instance for password hashing and verification.
        """
        self.user_repository = user_repository
        self.token_provider = token_provider
        self.hasher_provider = hasher_provider

    @handle_exceptions
    async def authenticate(self, auth_request: AuthRequestDTO) -> AuthResponseDTO:
        """
        Authenticate a user using the provided username and password.

        This method retrieves user data by username from the user repository,
        verifies if the user exists and is active, and checks the password using
        the hasher provider. Upon successful authentication, it generates both an
        access token and a refresh token, and returns them encapsulated in an
        AuthResponseDTO.

        Args:
            auth_request (AuthRequestDTO): The authentication request containing the username and password.

        Returns:
            AuthResponseDTO: An object containing the access token, token type ("Bearer"),
                             refresh token, and the access token's expiration time (e.g., 1800 seconds).

        Raises:
            UnauthorizedException: If the user does not exist, is inactive, or the password is incorrect.
        """
        user_data = await self.user_repository.get_current_user_by_name(
            auth_request.username
        )

        if not user_data:
            raise UnauthorizedException(
                message="Authentication failed",
                details="Invalid username or password",
                type_=ErrorTypes.AUTHENTICATION_FAILED,
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_data["is_active"] is False:
            raise UnauthorizedException(
                message="Authentication failed",
                details="User account is inactive",
                type_=ErrorTypes.INACTIVE_ACCOUNT,
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not await self.hasher_provider.verify(
            auth_request.password,
            user_data["password"],
        ):
            raise UnauthorizedException(
                message="Authentication failed",
                details="Invalid username or password",
                type_=ErrorTypes.AUTHENTICATION_FAILED,
                headers={"WWW-Authenticate": "Bearer"},
            )

        role_name = user_data["role_name"].upper()
        user_scopes = Scopes.ROLE_SCOPES.get(role_name, [])

        access_token, expires_in = await self.token_provider.generate_access_token(
            {
                "sub": user_data["username"],
                "scope": "access",
                "user_scopes": user_scopes,
                "role": user_data["role_name"].upper(),
                "department_id": user_data["department_id"],
            }
        )

        refresh_token = await self.token_provider.generate_refresh_token(
            {
                "sub": user_data["username"],
                "scope": "refresh",
            }
        )

        return AuthResponseDTO(
            access_token=access_token,
            token_type="Bearer",
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

    @handle_exceptions
    async def get_current_user(self, token: str) -> CurrentUserResponseDTO:
        """
        Retrieve the current user's information using an access token.

        This method verifies and decodes the provided access token, extracts the username,
        and obtains the associated user data from the repository. If the token is invalid,
        if the user does not exist, or if the user is inactive, an UnauthorizedException is raised.

        Args:
            token (str): The access token to validate.

        Returns:
            CurrentUserResponseDTO: A data transfer object containing the user's details including:
                                    id, username, employee name, role name, active status, creation, and update timestamps.

        Raises:
            UnauthorizedException: If the token is invalid, the user is not found, or the user is inactive.
        """
        payload = await self.token_provider.verify_and_decode_token(token)
        username = payload.get("sub")
        scope = payload.get("scope")

        if not username or scope != "access":
            raise UnauthorizedException(
                message="Token validation failed",
                details="Access token is invalid or has expired",
                type_=ErrorTypes.INVALID_TOKEN,
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = await self.user_repository.get_current_user_by_name(username)

        if not user_data:
            raise UnauthorizedException(
                message="User not found",
                details="The user associated with this token does not exist in the system",
                type_=ErrorTypes.USER_NOT_FOUND,
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_data["is_active"] is False:
            raise UnauthorizedException(
                message="Inactive account",
                details="The user account is inactive",
                type_=ErrorTypes.INACTIVE_ACCOUNT,
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_dto = CurrentUserResponseDTO(
            id=user_data["id"],
            username=user_data["username"],
            employee_name=user_data["employee_name"],
            role_name=user_data["role_name"],
            department_id=user_data["department_id"],
            is_active=user_data["is_active"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"],
        )

        user_dto._token_payload = payload

        return user_dto

    @handle_exceptions
    async def generate_refresh_access_token(
        self, refresh_token: str
    ) -> AuthResponseDTO:
        """
        Generate a new access token using a valid refresh token.

        This method first verifies and decodes the provided refresh token to extract
        the username, then retrieves the corresponding user data from the repository.
        If the refresh token is invalid, the user is not found, or if the user is inactive,
        an UnauthorizedException is raised. Upon successful validation, a new access token
        is generated while retaining the given refresh token.

        Args:
            refresh_token (str): The refresh token to use for generating a new access token.

        Returns:
            AuthResponseDTO: An object containing the new access token, token type ("Bearer"),
                             the existing refresh token, and the access token's expiration time (e.g., 1800 seconds).

        Raises:
            UnauthorizedException: If the refresh token is invalid, the user is not found, or the user is inactive.
        """
        payload = await self.token_provider.verify_and_decode_token(refresh_token)
        username = payload.get("sub")
        scope = payload.get("scope")

        if not username or scope != "refresh":
            raise UnauthorizedException(
                message="Token validation failed",
                details="Refresh token is invalid or has expired",
                type_=ErrorTypes.INVALID_REFRESH_TOKEN,
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = await self.user_repository.get_current_user_by_name(username)

        if not user_data:
            raise UnauthorizedException(
                message="User not found",
                details="The user associated with this token does not exist in the system",
                type_=ErrorTypes.USER_NOT_FOUND,
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_data["is_active"] is False:
            raise UnauthorizedException(
                message="Inactive account",
                details="The user account is inactive",
                type_=ErrorTypes.INACTIVE_ACCOUNT,
                headers={"WWW-Authenticate": "Bearer"},
            )

        role_name = user_data["role_name"].upper()
        user_scopes = Scopes.ROLE_SCOPES.get(role_name, [])

        new_access_token, expires_in = await self.token_provider.generate_access_token(
            {
                "sub": user_data["username"],
                "scope": "access",
                "user_scopes": user_scopes,
                "role": user_data["role_name"].upper(),
                "department_id": user_data["department_id"],
            }
        )

        return AuthResponseDTO(
            access_token=new_access_token,
            token_type="Bearer",
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

    @handle_exceptions
    async def get_current_user_with_scopes(
        self, token: str, required_scopes: list[str]
    ) -> CurrentUserResponseDTO:
        """
        Retrieve the current user's information and verify that the user has the required scopes.

        This method validates the provided access token and extracts the user's information.
        It then checks whether the token payload contains all of the specified required scopes.
        If any required scope is missing, or if the token is invalid, the user is not found,
        or the user is inactive, the method raises an appropriate exception.

        Args:
            token (str): The access token used for authentication.
            required_scopes (list[str]): A list of scopes that the user must have.

        Returns:
            CurrentUserResponseDTO: A data transfer object that contains the user's details,
                                    including their id, username, employee name, role name (in uppercase),
                                    active status, and timestamps for creation and update, along with
                                    the token payload for additional context.

        Raises:
            UnauthorizedException: If the token is invalid, the user is not found, or the user is inactive.
            ForbiddenException: If the user does not possess one or more of the required scopes.
        """
        payload = await self.token_provider.verify_and_decode_token(token)
        username = payload.get("sub")
        scope = payload.get("scope")

        if not username or scope != "access":
            raise UnauthorizedException(
                message="Token validation failed",
                details="Access token is invalid or has expired",
                type_=ErrorTypes.INVALID_TOKEN,
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = await self.user_repository.get_current_user_by_name(username)

        if not user_data:
            raise UnauthorizedException(
                message="User not found",
                details="The user associated with this token does not exist in the system",
                type_=ErrorTypes.USER_NOT_FOUND,
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_data["is_active"] is False:
            raise UnauthorizedException(
                message="Inactive account",
                details="The user account is inactive",
                type_=ErrorTypes.INACTIVE_ACCOUNT,
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_dto = CurrentUserResponseDTO(
            id=user_data["id"],
            username=user_data["username"],
            employee_name=user_data["employee_name"],
            role_name=user_data["role_name"].upper(),
            department_id=user_data["department_id"],
            is_active=user_data["is_active"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"],
        )

        if required_scopes:
            user_scopes = payload.get("user_scopes", [])
            for scope_required in required_scopes:
                if scope_required not in user_scopes:
                    raise ForbiddenException(
                        message="Permission denied",
                        details=f"User does not have the required permission: {scope_required}",
                    )

        return user_dto
