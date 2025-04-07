from abc import ABC, abstractmethod
from src.app.dto.request import AuthRequestDTO
from src.app.dto.response import UserResponseDTO, AuthResponseDTO


class IAuthService(ABC):

    @abstractmethod
    async def authenticate(self, auth_request: AuthRequestDTO) -> AuthResponseDTO:
        pass

    @abstractmethod
    async def get_current_user(self, token: str) -> UserResponseDTO:
        pass

    @abstractmethod
    async def generate_refresh_access_token(
        self, refresh_token: str
    ) -> AuthResponseDTO:
        pass
