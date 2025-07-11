from pydantic import BaseModel, Field


class AuthRequestDTO(BaseModel):
    """
    Data Transfer Object for authentication requests.
    """

    username: str = Field(
        ..., description="The username of the user.", examples=["johndoe", "janedoe"]
    )
    password: str = Field(..., description="The password of the user.")
