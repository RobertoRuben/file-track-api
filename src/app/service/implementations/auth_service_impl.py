from src.app.dto.request import AuthRequestDTO
from src.app.dto.response import UserResponseDTO, AuthResponseDTO
from src.app.service.interfaces import IAuthService
from src.app.repository.interfaces import IUserRepository
from src.app.security.auth.interface import ITokenProvider
from src.app.security.hasher.interface import IHasherProvider
from src.app.exception.decorator import handle_exceptions
from src.app.exception import UnauthorizedException


class AuthServiceImpl(IAuthService):
    """
    Implementation of the authentication service interface.
    Handles business logic for user authentication and token management.

    :ivar user_repository: Repository for user data operations
    :ivar token_provider: Provider for token generation and validation
    :ivar hasher_provider: Provider for password hashing and verification
    """

    def __init__(
        self,
        user_repository: IUserRepository,
        token_provider: ITokenProvider,
        hasher_provider: IHasherProvider,
    ):
        """
        Initialize the authentication service with required dependencies.

        :param user_repository: Repository for user data operations
        :param token_provider: Provider for token generation and validation
        :param hasher_provider: Provider for password hashing and verification
        """
        self.user_repository = user_repository
        self.token_provider = token_provider
        self.hasher_provider = hasher_provider

    @handle_exceptions
    async def authenticate(self, auth_request: AuthRequestDTO) -> AuthResponseDTO:
        """
        Authenticate a user with username and password.

        :param auth_request: The authentication request containing username and password
        :return: Authentication response with access and refresh tokens
        :raises UnauthorizedException: If credentials are invalid, user is inactive, or other auth failures
        """
        user_data = await self.user_repository.get_by_username(auth_request.username)
        if not user_data:
            raise UnauthorizedException(
                details=f"User or password is incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_data.is_active is False:
            raise UnauthorizedException(
                details=f"User is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not await self.hasher_provider.verify(
            auth_request.password, user_data.password
        ):
            raise UnauthorizedException(
                details=f"User or password is incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = await self.token_provider.generate_access_token(
            {
                "sub": user_data.username,
                "scope": "access",
            }
        )

        refresh_token = await self.token_provider.generate_refresh_token(
            {
                "sub": user_data.username,
                "scope": "refresh",
            }
        )

        return AuthResponseDTO(
            access_token=access_token,
            token_type="Bearer",
            refresh_token=refresh_token,
            expires_in=1800,
        )

    @handle_exceptions
    async def get_current_user(self, token: str) -> UserResponseDTO:
        """
        Retrieve the current user based on an access token.

        :param token: The access token to validate
        :return: User information as UserResponseDTO
        :raises UnauthorizedException: If token is invalid, user not found, or user is inactive
        """
        payload = await self.token_provider.verify_and_decode_token(token)
        username = payload.get("sub")
        scope = payload.get("scope")

        if not username or scope != "access":
            raise UnauthorizedException(
                details=f"Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = await self.user_repository.get_by_username(username)

        if not user_data:
            raise UnauthorizedException(
                details=f"User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_data.is_active is False:
            raise UnauthorizedException(
                details=f"User is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return UserResponseDTO(
            id=user_data.id,
            username=user_data.username,
            role_id=user_data.role_id,
            employee_id=user_data.employee_id,
            is_active=user_data.is_active,
            created_at=user_data.created_at,
            updated_at=user_data.updated_at,
        )

    @handle_exceptions
    async def generate_refresh_access_token(
        self, refresh_token: str
    ) -> AuthResponseDTO:
        """
        Generate a new access token using a valid refresh token.

        :param refresh_token: The refresh token to use for generating a new access token
        :return: Authentication response with new access token and existing refresh token
        :raises UnauthorizedException: If refresh token is invalid, user not found, or user is inactive
        """
        payload = await self.token_provider.verify_and_decode_token(refresh_token)
        username = payload.get("sub")
        scope = payload.get("scope")

        if not username or scope != "refresh":
            raise UnauthorizedException(
                details=f"Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = await self.user_repository.get_by_username(username)

        if not user_data:
            raise UnauthorizedException(
                details=f"User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user_data.is_active is False:
            raise UnauthorizedException(
                details=f"User is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )

        new_access_token = await self.token_provider.generate_access_token(
            {
                "sub": user_data.username,
                "scope": "access",
            }
        )

        return AuthResponseDTO(
            access_token=new_access_token,
            token_type="Bearer",
            refresh_token=refresh_token,
            expires_in=1800,
        )
