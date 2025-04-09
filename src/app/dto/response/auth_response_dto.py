from pydantic import BaseModel, Field


class AuthResponseDTO(BaseModel):
    """
    Data Transfer Object for authentication responses.
    """

    access_token: str = Field(..., description="The access token.")
    token_type: str = Field(..., description="The type of the token.")
    refresh_token: str | None = Field(default=None, description="The refresh token.")
    expires_in: int | None = Field(default=None, description="The expires in.")
