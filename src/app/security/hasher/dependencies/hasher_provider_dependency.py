from src.app.security.hasher.interface import HasherProvider
from src.app.security.hasher.implementations.hasher_provider_impl import (
    HasherProviderImpl,
)


async def get_hasher_provider() -> HasherProvider:
    """
    Dependency provider for the HasherProvider interface.

    This function provides an instance of HasherProviderImpl, which implements the Argon2 hashing algorithm.
    It is used as a dependency in FastAPI routes to ensure that the hashing provider is available for use.

    :return: An instance of HasherProviderImpl.
    """
    return HasherProviderImpl()
