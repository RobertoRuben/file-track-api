from abc import ABC, abstractmethod
from src.app.core.security.auth.model import CurrentUser
from src.app.core.security.auth.dto.request import AuthRequestDTO
from src.app.core.security.auth.dto.response import AuthResponseDTO


class IAuthService(ABC):
    """
    Interface for the authentication service.

    This abstract class defines the methods required for user authentication,
    token management, and user authorization. Implementations of this interface
    should provide the concrete business logic for verifying user credentials,
    retrieving user data, and generating or refreshing tokens.
    """

    @abstractmethod
    async def authenticate(self, auth_request: AuthRequestDTO) -> AuthResponseDTO:
        """
        Authenticate a user using the provided authentication request.

        The method should verify the user's credentials and generate an authentication
        response that includes the access token, refresh token, and token expiration details.

        Args:
            auth_request (AuthRequestDTO): The authentication request containing the username and password.

        Returns:
            AuthResponseDTO: A data transfer object containing the access token, token type ("Bearer"),
                             refresh token, and the expiration time of the access token.
        """
        pass

    @abstractmethod
    async def get_current_user(self, token: str) -> CurrentUser:
        """
        Retrieve the current user's information based on an access token.

        The method should validate and decode the provided access token and then retrieve
        the user's details from the data source.

        Args:
            token (str): The access token to be verified.

        Returns:
            CurrentUserResponseDTO: A data transfer object containing the current user's details,
                                    such as ID, username, employee name, role, and active status.
        """
        pass

    @abstractmethod
    async def generate_refresh_access_token(
        self, refresh_token: str
    ) -> AuthResponseDTO:
        """
        Generate a new access token using a valid refresh token.

        The method should verify the refresh token and, upon validation, generate a new access token.
        The existing refresh token is maintained in the response.

        Args:
            refresh_token (str): The refresh token provided for token renewal.

        Returns:
            AuthResponseDTO: A data transfer object containing the new access token, token type ("Bearer"),
                             the existing refresh token, and the expiration time of the new access token.
        """
        pass

    @abstractmethod
    async def get_current_user_with_scopes(
        self, token: str, required_scopes: list[str]
    ) -> CurrentUser:
        """
        Retrieve the current user's information and verify that the user has the required scopes.

        The method should validate the access token and check if it contains all the scopes
        specified in the required_scopes list. If the access token is invalid or the user does not
        possess one or more of the required scopes, appropriate exceptions should be raised.

        Args:
            token (str): The access token used for authentication.
            required_scopes (list[str]): A list of scopes that the user must have.

        Returns:
            CurrentUserResponseDTO: A data transfer object containing the current user's details,
                                    including the token payload for additional context.
        """
        pass
