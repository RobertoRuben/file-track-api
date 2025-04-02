from abc import ABC, abstractmethod


class HasherProvider(ABC):
    """
    Abstract interface for password encryption services.
    Provides methods for secure password hashing and verification.
    """

    @abstractmethod
    async def encrypt(self, plain_text: str) -> str:
        """
        Asynchronously encrypts a plain text password.

        Args:
            plain_text: The plain text password to be encrypted.

        Returns:
            A secure hash of the password.
        """
        pass

    @abstractmethod
    async def decrypt(self, plain_text: str, hashed_text: str) -> bool:
        """
        Asynchronously verifies if a plain text password matches a hashed password.
        This method doesn't actually decrypt the hash (which is impossible) but rather
        verifies if the plain text would produce the same hash.

        Args:
            plain_text: The plain text password to verify.
            hashed_text: The hashed password to compare against.

        Returns:
            True if the plain text matches the hash, False otherwise.
        """
        pass
