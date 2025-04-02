import asyncio
from src.app.config import settings
from src.app.security.hasher.interface import IHasherProvider
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class HasherProviderImpl(IHasherProvider):
    """
    Implementation of the HasherProvider interface using the Argon2 hashing algorithm.
    """

    def __init__(self):
        """
        Initialize the HasherProviderImpl with Argon2 configuration values from settings.

        The Argon2 hasher is configured with the following parameters:
          - time_cost: Controls the computational complexity.
          - memory_cost: Sets the memory usage in KiB.
          - parallelism: Defines the number of parallel threads.
          - hash_len: Specifies the length of the resulting hash in bytes.
          - salt_len: Specifies the length of the salt in bytes.
        """
        self.encryptor = PasswordHasher(
            time_cost=settings.ARGON2_TIME_COST,
            memory_cost=settings.ARGON2_MEMORY_COST,
            parallelism=settings.ARGON2_PARALLELISM,
            hash_len=settings.ARGON2_HASH_LEN,
            salt_len=settings.ARGON2_SALT_LEN,
        )

    async def encrypt(self, plain_text: str) -> str:
        """
        Hash the provided plain text using the Argon2 algorithm.

        :param plain_text: The plain text to be hashed.
        :return: A string representing the Argon2 hash of the plain text.
        """
        return await asyncio.to_thread(self.encryptor.hash, plain_text)

    async def verify(self, plain_text: str, hashed_text: str) -> bool:
        """
        Verify whether the given plain text matches the provided Argon2 hash.

        :param plain_text: The plain text to be verified.
        :param hashed_text: The Argon2-hashed text to compare against.
        :return: True if the plain text matches the hashed text; otherwise, False.
        """
        try:
            await asyncio.to_thread(self.encryptor.verify, hashed_text, plain_text)
            return True
        except VerifyMismatchError:
            return False
